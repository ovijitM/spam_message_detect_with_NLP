from flask import Flask, render_template, request, jsonify
from src.model.spam_filter import SpamFilter
import os

app = Flask(__name__)

spam_filter = None

def load_or_train_model():
    global spam_filter
    model_path = 'data/processed/spam_filter_model.pkl'
    
    if os.path.exists(model_path):
        spam_filter = SpamFilter.load_model(model_path)
    else:
        spam_filter = SpamFilter()
        spam_filter.train('data/raw/spam.csv')
        spam_filter.save_model(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_spam', methods=['POST'])
def check_spam():
    if not spam_filter:
        load_or_train_model()
    
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    prediction, probability = spam_filter.predict(message)
    
    return jsonify({
        'prediction': prediction,
        'probability': float(probability),
        'is_spam': prediction == 'spam'
    })

if __name__ == '__main__':
    load_or_train_model()
    app.run(debug=True) 