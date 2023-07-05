# Website Categorization
The purpose of this project is to detect the subject of Farsi's websites. Considering `Python3` for implementation, web-scraping packages such as `requests` and `beautifulsoup` are used to extract texts from websites and with the help of TF-IDF vectorizer, the most relevant words are linked to the websites with a score and word vectors are created. Then, with the help of machine learning algorithms, it compares and predicts the similarity vector of the words of the websites.

### Supported Languages
* Farsi (Persian)

### Requirements
* Python >= 3.9
* requests library
* beautifulsoup library
* scikit-learn library
