# Website Categorization
Website Topic Discovery: The goal of this project is recognition of the subject of Persian websites. Considering python for implementation, we utilize web-scraping packages such as selenium to crawl the websites from a pool of URLs. For each of the crawled web sites, we then apply preparations including stop-word removal, stemming, and tokenization to extract a collection keywords and sentences. After associating each keyword with a TF-IDF score, we use word embedding and NLP packages, and develop a classifier for detecting the website subject. Collecting labeled training data is a major challenge in this project, for which we consider unsupervised techniques and clustering algorithms such as Fuzzy C-Means over a pool of unlabeled documents, and use human intelligence for finalizing the labels.

### Supported Languages:
* Persian (فارسی)

#### Requirements:
* Python >= 3.10
* Selenium (Driver & Module)
* NLTK
