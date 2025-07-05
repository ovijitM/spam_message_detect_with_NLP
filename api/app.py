from flask import Flask, request, jsonify
import re
import string
import math
from collections import Counter

app = Flask(__name__)

# Common English stop words
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
    'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once'
}

class LightweightSpamFilter:
    def __init__(self):
        self.spam_words = {}
        self.ham_words = {}
        self.spam_count = 0
        self.ham_count = 0
        self.vocabulary = set()
        self.is_trained = False
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        words = [word for word in text.split() if word not in STOP_WORDS and len(word) > 2]
        return words
    
    def train(self):
        """Train the spam filter with a lightweight dataset"""
        training_data = [
            ("free money now click here urgent", "spam"),
            ("congratulations you won million dollars", "spam"),
            ("limited time offer click now", "spam"),
            ("urgent your account will be closed", "spam"),
            ("winner notification click claim prize", "spam"),
            ("call now free consultation", "spam"),
            ("credit card has been charged", "spam"),
            ("act now limited time", "spam"),
            ("earn money fast", "spam"),
            ("guarantee profit investment", "spam"),
            ("hello how are you today", "ham"),
            ("meeting tomorrow afternoon", "ham"),
            ("can you send report", "ham"),
            ("thanks for help yesterday", "ham"),
            ("looking forward weekend", "ham"),
            ("see you conference", "ham"),
            ("happy birthday great day", "ham"),
            ("project deadline next week", "ham"),
            ("lunch plans today", "ham"),
            ("good morning everyone", "ham")
        ]
        
        for text, label in training_data:
            words = self.preprocess_text(text)
            self.vocabulary.update(words)
            
            if label == "spam":
                self.spam_count += 1
                for word in words:
                    self.spam_words[word] = self.spam_words.get(word, 0) + 1
            else:
                self.ham_count += 1
                for word in words:
                    self.ham_words[word] = self.ham_words.get(word, 0) + 1
        
        self.is_trained = True
    
    def predict(self, text):
        """Predict if a text is spam or ham using Naive Bayes"""
        if not self.is_trained:
            self.train()
        
        words = self.preprocess_text(text)
        
        total_messages = self.spam_count + self.ham_count
        spam_prior = self.spam_count / total_messages
        ham_prior = self.ham_count / total_messages
        
        spam_score = math.log(spam_prior)
        ham_score = math.log(ham_prior)
        
        total_spam_words = sum(self.spam_words.values())
        total_ham_words = sum(self.ham_words.values())
        vocab_size = len(self.vocabulary)
        
        for word in words:
            spam_word_count = self.spam_words.get(word, 0)
            ham_word_count = self.ham_words.get(word, 0)
            
            spam_word_prob = (spam_word_count + 1) / (total_spam_words + vocab_size)
            ham_word_prob = (ham_word_count + 1) / (total_ham_words + vocab_size)
            
            spam_score += math.log(spam_word_prob)
            ham_score += math.log(ham_word_prob)
        
        if spam_score > ham_score:
            prediction = "spam"
            exp_spam = math.exp(spam_score)
            exp_ham = math.exp(ham_score)
            probability = exp_spam / (exp_spam + exp_ham)
        else:
            prediction = "ham"
            exp_spam = math.exp(spam_score)
            exp_ham = math.exp(ham_score)
            probability = exp_ham / (exp_spam + exp_ham)
        
        return prediction, probability

# Initialize the spam filter
spam_filter = LightweightSpamFilter()

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Spam Detection</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        textarea { width: 100%; height: 100px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        button { background: #007cba; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; width: 100%; margin-top: 10px; }
        button:hover { background: #005a8a; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; text-align: center; display: none; }
        .spam { background: #ffe6e6; color: #d00; border: 1px solid #ffb3b3; }
        .ham { background: #e6ffe6; color: #080; border: 1px solid #b3ffb3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Spam Detection</h1>
        <textarea id="message" placeholder="Enter your message here..."></textarea>
        <button onclick="checkSpam()">Check for Spam</button>
        <div id="result" class="result"></div>
    </div>
    <script>
        async function checkSpam() {
            const message = document.getElementById('message').value;
            const result = document.getElementById('result');
            
            if (!message.trim()) {
                alert('Please enter a message');
                return;
            }
            
            try {
                const response = await fetch('/api/check_spam', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const prob = (data.probability * 100).toFixed(1);
                    const className = data.is_spam ? 'spam' : 'ham';
                    const resultText = data.is_spam ? 'SPAM' : 'NOT SPAM';
                    
                    result.className = `result ${className}`;
                    result.innerHTML = `<strong>${resultText}</strong><br>Confidence: ${prob}%`;
                    result.style.display = 'block';
                } else {
                    result.className = 'result spam';
                    result.innerHTML = `Error: ${data.error}`;
                    result.style.display = 'block';
                }
            } catch (error) {
                result.className = 'result spam';
                result.innerHTML = `Error: ${error.message}`;
                result.style.display = 'block';
            }
        }
    </script>
</body>
</html>'''

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'model_trained': spam_filter.is_trained})

@app.route('/api/check_spam', methods=['POST'])
def check_spam():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        if not spam_filter.is_trained:
            spam_filter.train()
        
        prediction, probability = spam_filter.predict(message)
        
        return jsonify({
            'prediction': prediction,
            'probability': float(probability),
            'is_spam': prediction == 'spam'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
