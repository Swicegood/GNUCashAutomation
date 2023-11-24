import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import import_map  # import_map is a module you have that provides the getImportMap function

class TransactionCategorizer:
    def __init__(self, account):
        # Load data for the account
        bayes_data = import_map.getImportMap(account)
        self.data_df = pd.DataFrame(bayes_data)
        
        # Train the model with the data
        self.clf, self.vectorizer, self.label_encoder = self.train_model(self.data_df)
    
    def train_model(self, data):
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
    
    def getCategory(self, transaction_desc, confidence_threshold=0.27):
        # Check for an exact match in the training data first
        if transaction_desc in self.data_df['desc'].values:
            return self.data_df[self.data_df['desc'] == transaction_desc]['category'].values[0]
        
        # Vectorize the transaction description
        trans_desc_vec = self.vectorizer.transform([transaction_desc])
        
        # Predict the category probabilities
        predicted_probabilities = self.clf.predict_proba(trans_desc_vec)
        
        # Get the best category and its associated probability
        best_cat_index = predicted_probabilities.argmax()
        best_cat_probability = predicted_probabilities.max()
        
        # Return the category only if the probability exceeds the threshold
        if best_cat_probability >= confidence_threshold:
            return self.label_encoder.inverse_transform([best_cat_index])[0]
        else:
            return None

if __name__ == "__main__":
    # Initialize the categorizer for a specific account
    categorizer = TransactionCategorizer(account='American Express *1008')

    # Example usage
    transaction_desc = "SHELL"

    # Predict category with the trained model
    predicted_category_guid = categorizer.getCategory(transaction_desc)

    # Convert the predicted category GUID to a human-readable name
    predicted_account_name = import_map.getAccountNameFromGuid(predicted_category_guid)

    # Output the category
    print(f"The category for the transaction description '{transaction_desc}' is: {predicted_account_name}")
