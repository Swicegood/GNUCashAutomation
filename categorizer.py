import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import numpy as np
import import_map  # import_map is a module you have that provides the getImportMap function

# Re-create the example map.csv with a few entries
example_data = [{
    'desc': 'AMZN',
    'category': 'lkajfldasd f9a8s7f0sad7fas',
    'count': 8
}, {
    'desc': 'WALMART',
    'category': 'a0d9fasd9fsiadpfj08sdafus8',
    'count': 5
}, {
    'desc': 'FOOD Lion',
    'category': 'asd98asd9fasd9f7sad09f7sdfs',
    'count': 1
}]
example_df = pd.DataFrame(example_data)

def train_model(data):
    # Preprocess the data
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data['desc'])
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data['category'])

    # Create sample weights based on count
    sample_weight = data['count'].values

    # Train the classifier
    clf = MultinomialNB()
    clf.fit(X, y, sample_weight=sample_weight)

    return clf, vectorizer, label_encoder


bayes_data = import_map.getImportMap(account='American Express *1008')
bayes_data_df = pd.DataFrame(bayes_data)
# Train the model once and store the trained components
clf, vectorizer, label_encoder = train_model(bayes_data_df)

# Define the getCategory function with confidence check and exact match check
def getCategory(transaction_desc, clf, vectorizer, label_encoder, confidence_threshold=0.27):
    # Check for an exact match in the training data first
    if transaction_desc in bayes_data_df['desc'].values:
        return bayes_data_df[bayes_data_df['desc'] == transaction_desc]['category'].values[0]

    # Vectorize the transaction description
    trans_desc_vec = vectorizer.transform([transaction_desc])

    # Predict the category probabilities
    predicted_probabilities = clf.predict_proba(trans_desc_vec)

    # Get the best category and its associated probability
    best_cat_index = predicted_probabilities.argmax()
    best_cat_probability = predicted_probabilities.max()

    # Return the category only if the probability exceeds the threshold
    if best_cat_probability >= confidence_threshold:
        return label_encoder.inverse_transform([best_cat_index])[0]
    else:
        return None

# Example usage
transaction_desc = "SHELL"

# Predict category with the trained model
predicted_category = getCategory(transaction_desc, clf, vectorizer, label_encoder)

predicted_account_name = import_map.getAccountNameFromGuid(predicted_category)

# Output the category
print(f"The category for the transaction description '{transaction_desc}' is: {predicted_account_name}")
