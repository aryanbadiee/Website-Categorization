import csv
import pandas as pd
import matplotlib.pyplot as plt
from category_recognizer import reader


def clean_data(data: list) -> list:
    """ cleaning data """

    for elem in data.copy():
        if elem[1] == '1':
            data.remove(elem)

    return data


def bar(data: list, title: str):
    data = pd.DataFrame(data, columns=["word", "repetition"])
    # print(data.shape)

    plt.bar(data["word"], data["repetition"])
    plt.title(title)
    plt.xticks(rotation=90)
    plt.xlabel('words')
    plt.ylabel('repetitions')
    plt.show()


if __name__ == '__main__':
    d = reader('../datasets/website_words.csv')
    bar(clean_data(d), 'bar')
