# Standard libraries:
import csv
import pickle
from typing import AnyStr, Iterable

# Other libraries:
import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


class WebsiteCategorization:
    """ This class provides facilities for training and predicting the category of websites """

    def __init__(self, unique_categories: Iterable, /):
        # Category to ID:
        cat2id = dict[str, int]()
        for i, category in enumerate(unique_categories):
            cat2id[category] = i

        # ID to category:
        id2cat = dict[int, str]()
        for category, i in cat2id.items():
            id2cat[i] = category

        self.cat2id = cat2id
        self.id2cat = id2cat

    def train(self, train_data: dict[str, list], /) -> None:
        """ Trains a model """

        # Collects training texts and IDs:
        train_texts = list[str]()
        train_ids = list[int]()
        for category, domains in train_data.items():
            text = ''
            for domain in domains:
                text += extract_text(domain) + ' '

            train_texts.append(text.strip())
            train_ids.append(self.cat2id[category])

        # Creates feature vectors using TF-IDF vectorization:
        vectorizer = TfidfVectorizer(
            strip_accents="unicode",
            analyzer="word",
            max_df=.25, min_df=.0,  # [0.0, 0.25] to remove stopwords!
            # max_features=256
        )
        train_vectors = vectorizer.fit_transform(train_texts)

        # Trains a linear support vector classifier:
        classifier = LinearSVC(dual='auto')
        classifier.fit(train_vectors, train_ids)

        self.vectorizer = vectorizer
        self.classifier = classifier

    def predict(self, domain: str, /) -> tuple[str, int]:
        """ Predicts the category of the domain and the confidence score """

        text = extract_text(domain)

        text_vector = self.vectorizer.transform([text])
        scores = self.classifier.decision_function(text_vector)[0]
        category_id = np.argmax(scores)

        return self.id2cat[category_id], scores[category_id]


def extract_text(domain: str, /) -> str:
    """ Extracts text from the domain """

    response = requests.get(domain, timeout=120)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    return text


def save(model, model_path: AnyStr, /) -> None:
    """ Saves the model """

    with open(model_path, 'wb') as file:
        pickle.dump(model, file)


def load(model_path: AnyStr, /) -> WebsiteCategorization:
    """ Loads the model """

    with open(model_path, 'rb') as file:
        return pickle.load(file)


if __name__ == "__main__":
    # Obtains data:
    data = dict[str, list]()
    with open("../datasets/dataset.csv", 'rt') as file_:
        csv_reader = csv.reader(file_)
        csv_reader.__next__()  # Skips header!

        for domain_, category_ in csv_reader:
            if not data.get(category_):  # Doesn't exist!
                data[category_] = [domain_]
            else:  # Exists!
                data[category_].append(domain_)

    # Builds and trains the model:
    cls = WebsiteCategorization(data.keys())
    cls.train(data)

    # Saves the model:
    # save(cls, "../model.ab3")

    # Loads the model:
    # cls = load("../model.ab3")

    # Predicts the category of the domain and the confidence score:
    sample_domain = "https://du.ac.ir"
    predicted_category, conf = cls.predict(sample_domain)
    print(
        f"The category of {sample_domain} is {predicted_category}",
        f"The confidence score is {conf}",
        sep='\n'
    )
