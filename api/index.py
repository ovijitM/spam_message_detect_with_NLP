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
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        # Split into words and remove stop words
        words = [word for word in text.split() if word not in STOP_WORDS and len(word) > 2]
        return words
    
    def train(self):
        """Train the spam filter with a lightweight dataset"""
        # Training data: (message, label)
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
        
        # Process training data
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
        
        # Calculate probabilities
        total_messages = self.spam_count + self.ham_count
        spam_prior = self.spam_count / total_messages
        ham_prior = self.ham_count / total_messages
        
        # Calculate log probabilities to avoid underflow
        spam_score = math.log(spam_prior)
        ham_score = math.log(ham_prior)
        
        total_spam_words = sum(self.spam_words.values())
        total_ham_words = sum(self.ham_words.values())
        vocab_size = len(self.vocabulary)
        
        for word in words:
            # Laplace smoothing
            spam_word_count = self.spam_words.get(word, 0)
            ham_word_count = self.ham_words.get(word, 0)
            
            spam_word_prob = (spam_word_count + 1) / (total_spam_words + vocab_size)
            ham_word_prob = (ham_word_count + 1) / (total_ham_words + vocab_size)
            
            spam_score += math.log(spam_word_prob)
            ham_score += math.log(ham_word_prob)
        
        # Determine prediction
        if spam_score > ham_score:
            prediction = "spam"
            # Convert log probabilities back to regular probabilities
            exp_spam = math.exp(spam_score)
            exp_ham = math.exp(ham_score)
            probability = exp_spam / (exp_spam + exp_ham)
        else:
            prediction = "ham"
            exp_spam = math.exp(spam_score)
            exp_ham = math.exp(ham_score)
            probability = exp_ham / (exp_spam + exp_ham)
        
        return prediction, probability

# Global spam filter instance
spam_filter = LightweightSpamFilter()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spam Detection with NLP</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 {
                text-align: center;
                color: #4a5568;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #4a5568;
            }
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 16px;
                resize: vertical;
                min-height: 120px;
                box-sizing: border-box;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                display: none;
            }
            .spam {
                background: #fed7d7;
                color: #c53030;
                border: 2px solid #feb2b2;
            }
            .ham {
                background: #c6f6d5;
                color: #22543d;
                border: 2px solid #9ae6b4;
            }
            .loading {
                display: none;
                text-align: center;
                margin-top: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Spam Detection with NLP</h1>
            <form id="spamForm">
                <div class="form-group">
                    <label for="message">Enter your message to check:</label>
                    <textarea id="message" name="message" placeholder="Type your message here..." required></textarea>
                </div>
                <button type="submit">Check for Spam</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing message...</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>

        <script>
            document.getElementById('spamForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const message = document.getElementById('message').value;
                const button = document.querySelector('button');
                const loading = document.getElementById('loading');
                const result = document.getElementById('result');
                
                // Show loading state
                button.disabled = true;
                loading.style.display = 'block';
                result.style.display = 'none';
                
                try {
                    const response = await fetch('/api/check_spam', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        const probability = (data.probability * 100).toFixed(1);
                        const resultClass = data.is_spam ? 'spam' : 'ham';
                        const resultText = data.is_spam ? 'SPAM' : 'NOT SPAM';
                        const emoji = data.is_spam ? '⚠️' : '✅';
                        
                        result.className = `result ${resultClass}`;
                        result.innerHTML = `
                            ${emoji} <strong>${resultText}</strong><br>
                            <small>Confidence: ${probability}%</small>
                        `;
                        result.style.display = 'block';
                    } else {
                        throw new Error(data.error || 'An error occurred');
                    }
                } catch (error) {
                    result.className = 'result spam';
                    result.innerHTML = `❌ Error: ${error.message}`;
                    result.style.display = 'block';
                } finally {
                    button.disabled = false;
                    loading.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/health')
def health_check():
    try:
        return jsonify({
            'status': 'healthy',
            'message': 'Spam detection API is running',
            'model_trained': spam_filter.is_trained
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/check_spam', methods=['POST'])
def check_spam():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Ensure the model is trained
        if not spam_filter.is_trained:
            spam_filter.train()
        
        prediction, probability = spam_filter.predict(message)
        
        return jsonify({
            'prediction': prediction,
            'probability': float(probability),
            'is_spam': prediction == 'spam'
        })
    except Exception as e:
        # Better error logging
        import traceback
        error_details = traceback.format_exc()
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'details': error_details
        }), 500

# Export the app for Vercel
app = app

# For local development
if __name__ == '__main__':
    app.run(debug=True)
