# Website Categorization
The purpose of this project is to detect the subject of Persian's websites. Considering `Python3` for implementation, web-scraping packages such as `requests` and `beautifulsoup` are used to extract text from websites and with the help of TF-IDF vectorizer, the most relevant words are linked to websites and words vectors are created. Then, with the help of machine learning algorithms, it compares and predicts the similarity words vectors of the websites.

### Supported Languages
* Persian (Farsi)

### Requirements
* Python >= 3.9
* beautifulsoup4==4.12.3
* certifi==2023.11.17
* charset-normalizer==3.3.2
* idna==3.6
* joblib==1.3.2
* numpy==1.26.3
* PySocks==1.7.1
* requests==2.31.0
* scikit-learn==1.4.0
* scipy==1.11.4
* soupsieve==2.5
* threadpoolctl==3.2.0
* urllib3==2.1.0