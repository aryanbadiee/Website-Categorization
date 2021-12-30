# standard library:
import random
import csv
from os import path, scandir
from urllib.parse import urlparse
from typing import AnyStr, Optional

# other library:
import pause
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class WebsiteClassification:
    """ website classification class """

    def __init__(self, dataset: AnyStr, proxy: Optional[str] = None):
        self.dataset = dataset
        self.proxy = proxy

        self.categories, self.stop_words, self.domains = self.__prepare_datasets()
        self.driver = self.__create_driver("chrome")

    def __prepare_datasets(self) -> tuple:
        """ prepares datasets """

        # categories:
        categories = dict[str, list]()
        for element in scandir(path.join(self.dataset, "categories")):
            if element.is_file():  # just file
                with open(element.path, encoding="UTF-8") as file:
                    categories[element.name.removesuffix(".txt")] = file.read()\
                        .splitlines(keepends=False)

        # stop-words:
        stop_words = list[str]()
        for element in scandir(path.join(self.dataset, "stop_words")):
            if element.is_file():  # just file
                with open(element.path, encoding="UTF-8") as file:
                    stop_words.extend(file.read().splitlines(keepends=False))

        # domains:
        domains = list[tuple]()
        for element in scandir(path.join(self.dataset, "domains")):
            if element.is_file():  # just file
                with open(element.path, encoding="UTF-8") as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)  # ignore head
                    for row in csv_reader:
                        domains.append(row)

        return categories, stop_words, domains

    def __create_driver(self, driver_type: str):
        """ makes browser driver """

        if driver_type == "chrome":
            options = webdriver.ChromeOptions()

            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            if self.proxy is not None:  # set proxy
                options.add_argument('--proxy-server=%s' % self.proxy)

            driver = webdriver.Chrome(
                executable_path="../browser_driver/chromedriver", options=options
            )

            return driver
        else:
            raise TypeError(f"not supported {driver_type} driver!")

    def page_source(self, url: str) -> str:
        """ gets web source code from an url """

        self.driver.get(url)
        pause.milliseconds(1_500)  # wait to load complete!

        return self.driver.page_source.lower()

    def classification(self, url: str) -> Optional[str]:
        """ tries to set a category for the domain """

        domain = urlparse(url).netloc.lower()
        print(f"{domain = }")

        try:
            page_source = self.page_source(url)
        except Exception as ex:
            print(ex)
            return  # or `return None`

        # find all links from website:
        web_elems = self.driver.find_elements(by=By.XPATH, value=".//a[@href]")

        # find internal links:
        internal_links = set[str]()
        for web_elem in web_elems:
            link = web_elem.get_attribute("href")
            if domain in urlparse(link).netloc.lower():
                internal_links.add(link)

        print('-' * 60)  # separator line

        internal_links = tuple(internal_links)  # convert set to tuple
        print('The number of internal links for', domain, '=', len(internal_links))
        selected_links = random.sample(internal_links, k=len(internal_links) // 4) \
            if len(internal_links) <= 200 else \
            random.sample(internal_links, k=50)
        print('The number of selected links for', domain, '=', len(selected_links))

        print('-' * 60)  # separator line

        repetitions = dict()

        # main page:
        for category, words in self.categories.items():
            word_count = 0
            for word in words:
                if word in page_source.lower():
                    word_count += 1

            repetitions[category] = word_count

        # selected links:
        for link in selected_links:
            try:
                page_source = self.page_source(link)
                for category, words in self.categories.items():
                    word_count = 0
                    for word in words:
                        if word in page_source.lower():
                            word_count += 1

                    repetitions[category] += word_count
            except Exception as ex:
                print(ex)
                continue

        total_words = sum(repetitions.values())
        for category, repetition in repetitions.items():
            print('%', format(repetition / total_words * 10 ** 2, '.2f'),
                  " for \"%(category)s\"" % {"category": category}, sep='')

        target_category = max(repetitions, key=lambda e: repetitions[e])
        return target_category

    def quit_driver(self) -> None:
        """ quits driver """

        self.driver.quit()  # quit driver!


if __name__ == "__main__":
    website_classification = WebsiteClassification("../datasets")

    for d, real_subject in random.sample(website_classification.domains, k=5):
        subject = website_classification.classification(d)
        print(
            '-' * 60,
            "Real Subject: %(domain)s" % {"domain": real_subject},
            "Predicted Subject: %(domain)s" % {"domain": subject},
            sep='\n',
            end='\n' + '*' * 60 + '\n'
        )

    website_classification.quit_driver()  # quit driver
