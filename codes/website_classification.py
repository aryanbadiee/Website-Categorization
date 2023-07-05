# Standard libraries:
import csv
from typing import Optional

# Other libraries:
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


def extract_text(domain) -> str:
    """ Extracts text from a website """

    response = requests.get(domain)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()  # or soup.text

    return text


def trainer() -> tuple:
    """ Trains a model for prediction """

    # Collects training texts and labels:
    train_texts = list[str]()
    train_labels = list[int]()
    for data in training_data:
        train_texts.append(extract_text(data['domain']))
        train_labels.append(categories[data['category']])

    # Creates feature vectors using TF-IDF vectorization:
    vectorizer = TfidfVectorizer(min_df=.0, max_df=.25)  # [0.0, 0.25] to remove stop words!
    train_vectors = vectorizer.fit_transform(train_texts)

    # Trains a linear support vector classifier:
    classifier = LinearSVC(dual='auto')
    classifier.fit(train_vectors, train_labels)

    return vectorizer, classifier


def predictor(domain) -> Optional[str]:
    """ Predicts the category of a website """

    text = extract_text(domain)

    text_vector = vec.transform([text])
    category_id = cls.predict(text_vector)[0]

    for category, _id in categories.items():
        if _id == category_id:
            return category


if __name__ == "__main__":
    # Collects the train data:
    training_data = list[dict]()
    categories = dict[str, int]()
    with open("../datasets/dataset.csv", 'rt') as file:
        csv_reader = csv.reader(file)
        csv_reader.__next__()  # Skips header!

        i = 0
        for d, c in csv_reader:
            training_data.append({"domain": d, "category": c})
            if not categories.get(c):  # New category!
                categories[c] = i
                i += 1

    vec, cls = trainer()  # Trains the model

    # Example usage:
    test_domain = "https://javacup.ir"
    predicted_category = predictor(test_domain)
    print('Predicted category:', predicted_category)
