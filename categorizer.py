import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import import_map

# Re-create the example map.csv with a few entries
example_data = [{
    'desc': 'AMZN',
    'category': 'lkajfldasd f9a8s7f0sad7fas',
    'count': 8
}, {
    'desc': 'WALMART',
    'category': 'a0d9fasd9fsiadpfj08sdafus8'
    'count': 5
}, {
    'desc': 'FOOD Lion',
    'category': 'asd98asd9fasd9f7sad09f7sdfs'
    'count': 1}]
example_df = pd.DataFrame(example_data)

# Function to update the map.csv with a new transaction
# def update_map(transaction, category):
#     # Load the existing map
#     map_df = pd.read_csv(map_file_path)
    
#     # Append the new transaction to the dataframe
#     new_entry = pd.DataFrame({'desc': [transaction['desc']], 'category': [category]})
#     updated_df = pd.concat([map_df, new_entry], ignore_index=True)
    
#     # Save the updated dataframe back to CSV
#     updated_df.to_csv(map_file_path, index=False)
#     return updated_df

# Function to train and return the Naive Bayes model, vectorizer, and label encoder
# def train_model(map_file_path):
#     # Load the map from the CSV file
#     map_df = pd.read_csv(map_file_path)
    
#     # Preprocess the data
#     vectorizer = CountVectorizer()
#     X = vectorizer.fit_transform(map_df['desc'])
#     label_encoder = LabelEncoder()
#     y = label_encoder.fit_transform(map_df['category'])
    
#     # Train the classifier
#     clf = MultinomialNB()
#     clf.fit(X, y)
    
#     return clf, vectorizer, label_encoder


def train_model(account):
    # Load the map from the list
    bayes_map = import_map.getImportMap(account)
    map_df = bayes_map
    
    # Preprocess the data
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(map_df['desc'])
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(map_df['category'])
    
    #train on each data in map_df number of times in count.value

    # Train the classifier
    clf = MultinomialNB()
    clf.fit(X, y)
    
    return clf, vectorizer, label_encoder


# Train the model once and store the trained components
clf, vectorizer, label_encoder = train_model(account="Amex")

# Define the getCategory function with confidence check and exact match check
def getCategory(transaction, clf, vectorizer, label_encoder, confidence_threshold=0.27):
    # Check for an exact match in the training data first
    if transaction["desc"] in example_df['desc'].values:
        return example_df[example_df['desc'] == transaction["desc"]]['category'].values[0]
    
    # Vectorize the transaction description
    trans_desc_vec = vectorizer.transform([transaction["desc"]])
    
    # Predict the category probabilities
    predicted_probabilities = clf.predict_proba(trans_desc_vec)
    
    # Print the distribution of probabilities
    print("Distribution of category probabilities:")
    for category, probability in zip(label_encoder.classes_, predicted_probabilities.flatten()):
        print(f"{category}: {probability:.4f}")
    
    # Get the best category and its associated probability
    best_cat_index = predicted_probabilities.argmax()
    best_cat_probability = predicted_probabilities.max()
    
    # Return the category only if the probability exceeds the threshold
    if best_cat_probability >= confidence_threshold:
        return label_encoder.inverse_transform([best_cat_index])[0]
    else:
        return None

# Example usage
transaction = {
    "desc": "AMZN",
    "memo": "BOOK PURCHASE"
}

# Predict category with the trained model
predicted_category = getCategory(transaction, clf, vectorizer, label_encoder)

# Output the category
print(f"The category for the transaction '{transaction['desc']}' is: {predicted_category}")
