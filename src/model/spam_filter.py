import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import pickle

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class SpamFilter:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text):
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        clean_words = [word.lower() for word in nopunc.split() if word.lower() not in self.stop_words]
        return ' '.join(clean_words)
    
    def train(self, data_path):
        df = pd.read_csv(data_path, sep='\t', header=None, names=['label', 'message'])
        df['clean_message'] = df['message'].apply(self.clean_text)
        X_train, X_test, y_train, y_test = train_test_split(df['clean_message'], df['label'], test_size=0.2, random_state=42)
        X_train_counts = self.vectorizer.fit_transform(X_train)
        X_test_counts = self.vectorizer.transform(X_test)
        self.classifier.fit(X_train_counts, y_train)
        y_pred = self.classifier.predict(X_test_counts)
        print("\nModel Evaluation:")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        return self
    
    def predict(self, message):
        clean_message = self.clean_text(message)
        message_counts = self.vectorizer.transform([clean_message])
        prediction = self.classifier.predict(message_counts)[0]
        probability = self.classifier.predict_proba(message_counts).max()
        return prediction, probability
    
    def save_model(self, model_path='spam_filter_model.pkl'):
        model_data = {'vectorizer': self.vectorizer, 'classifier': self.classifier}
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
    
    @classmethod
    def load_model(cls, model_path='spam_filter_model.pkl'):
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        spam_filter = cls()
        spam_filter.vectorizer = model_data['vectorizer']
        spam_filter.classifier = model_data['classifier']
        return spam_filter

def main():
    # Example usage
    spam_filter = SpamFilter()
    
    # Train the model (uncomment and modify the path as needed)
    # spam_filter.train('path_to_your_dataset/SMSSpamCollection')
    
    # Example messages to test
    test_messages = [
        "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 for entry question(std txt rate)T&C's apply",
        "Hey, are you coming to the meeting tomorrow?",
        "URGENT! You have won a 1 week FREE membership in our £100,000 prize Jackpot! Txt the word: CLAIM to No: 81010 T&C www.dbuk.net",
        "Ok, I'll see you later then!"
    ]
    
    print("\nTesting the spam filter:")
    print("-" * 50)
    for message in test_messages:
        prediction, probability = spam_filter.predict(message)
        print(f"\nMessage: {message[:100]}...")
        print(f"Prediction: {prediction}")
        print(f"Confidence: {probability:.2%}")

if __name__ == "__main__":
    main() 