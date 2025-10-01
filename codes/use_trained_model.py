from website_classification import WebsiteCategorization


if __name__ == "__main__":
    # Loads the model
    cls = WebsiteCategorization.load("../model/pre-trained_model.ab3")

    # Predicts the category of the domain and the confidence score
    sample_domain = "https://ui.ac.ir/"
    predicted_category, conf = cls.predict(sample_domain)
    print(f"The category of {sample_domain} is {predicted_category}",
          f"The confidence score is {conf:.4f}",
          sep='\n')
