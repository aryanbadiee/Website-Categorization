# Website Categorization
The purpose of this project is to detect the subject of Persian websites. Considering Python for implementation, web-scraping packages such as Selenium are used to crawl websites from a set of URLs. For each crawled website, preparations are made, including stop-words removal and tokenization to extract words and sentences. After associating each keyword with the TF-IDF score, the category with most score set to the subject of the website. Keywords for each category and stop-words are collected with human intelligence.

### Supported Languages:
* Persian (فارسی)

#### Requirements:
* Python >= 3.9
* Selenium (Driver & Module)
* NLTK
