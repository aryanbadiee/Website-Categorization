import requests
import re
import csv
from bs4 import BeautifulSoup


def scrape(url: str) -> BeautifulSoup:
    """ makes BeautifulSoup object """

    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def separate_words(txt: str) -> dict[str, int]:
    """ splits words by white space and count repetition """

    # replace anything except words with whitespace:
    txt = re.sub(r'[^\w]', ' ', txt)

    words_repetition = dict[str, int]()
    for word in txt.split():
        if not words_repetition.get(word):  # not exists
            words_repetition[word] = 1
        else:  # exists
            words_repetition[word] += 1

    return words_repetition


def sort_words(words: dict[str, int]) -> list:
    """ sorts words based on repetition (Descending) """

    return sorted(words.items(), key=lambda e: e[1], reverse=True)


def write_on_file(filename: str, words: list, *, file_type: str = "csv"):
    """ writes words and its repetitions on file """

    if file_type == "csv":
        with open(filename, 'wt', encoding="UTF-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(('word', 'number_of_repetition'))  # write head
            csv_writer.writerows(words)
    else:
        raise TypeError("not supported file type!")


if __name__ == "__main__":
    website = 'https://www.chavoosh.com/' \
              '%D8%AA%D8%AD%D9%84%DB%8C%D9%84-%D8%AF%D8%A7%D8%AF%D9%87-' \
              '%D9%87%D8%A7%DB%8C-%D9%85'\
              '%D8%AE%D8%A7%D8%A8%D8%B1%D8%A7%D8%AA%DB%8C-%D9%BE%DA%98%D9%88%D8%A7%DA%A9/'

    soup = scrape(website)
    web_elements = soup.find_all('p', limit=3)

    # take out the texts in 'p' tag:
    text = ''
    for web_element in web_elements:
        text += web_element.text

    website_words = separate_words(text)
    website_words = sort_words(website_words)

    write_on_file('../datasets/website_words.csv', website_words)
