# standard library:
import random
from os import path, listdir
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

        self.categories = self.prepare_categories()
        self.driver = self.create_driver("chrome")

    def prepare_categories(self) -> dict[str, list]:
        """ prepares categories """

        categories = dict[str, list]()

        category_files = listdir(self.dataset)
        for category_file in category_files:
            with open(path.join(self.dataset, category_file), encoding="UTF-8") as file:
                categories[category_file.removesuffix(".txt")] = file.read()\
                    .splitlines(keepends=False)

        return categories

    def create_driver(self, driver_type: str):
        """ makes browser driver """

        if driver_type == "chrome":
            options = webdriver.ChromeOptions()

            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            if self.proxy is not None:  # set proxy
                options.add_argument('--proxy-server=%s' % self.proxy)

            driver = webdriver.Chrome(options=options,
                                      service=Service(executable_path="../browser_driver"
                                                                      "/chromedriver"))

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
        internal_links = list()
        for web_elem in web_elems:
            link = web_elem.get_attribute("href")
            if domain in urlparse(link).netloc.lower():
                internal_links.append(link)

        print('-' * 60)  # separator line

        print('The number of internal links for', domain, '=', len(internal_links))
        selected_links = random.sample(internal_links, k=len(internal_links) // 4)
        print('The number of selected links for', domain, '=', len(selected_links))

        print('-' * 60)  # separator line

        repetitions = dict()

        # main page:
        for category, words in self.categories.items():
            word_count = 0
            for word in words:
                word_count += page_source.count(word.lower())

            repetitions[category] = word_count

        # selected links:
        for link in selected_links:
            try:
                page_source = self.page_source(link)
                for category, words in self.categories.items():
                    word_count = 0
                    for word in words:
                        word_count += page_source.count(word.lower())

                    repetitions[category] += word_count
            except Exception as ex:
                print(ex)
                continue

        total_words = sum(repetitions.values())
        for category, repetition in repetitions.items():
            print('%', format(repetition / total_words * 10 ** 2, '.2f'),
                  " for \"%(category)s\"" % {"category": category}, sep='')

        self.driver.quit()  # quit driver!

        target_category = max(repetitions, key=lambda e: repetitions[e])
        return target_category


if __name__ == "__main__":
    website_classification = WebsiteClassification("../datasets")
    subject = website_classification.classification("https://komsera.com")

    print('-' * 60, subject, sep='\n')
