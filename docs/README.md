# Spam Message Detector

A web application that uses Natural Language Processing (NLP) and Machine Learning to detect spam messages. The project is organized into four distinct phases, each focusing on a specific aspect of the application.

## Project Phases

### Phase 1: Model Creation
- Core spam detection model implementation
- Text preprocessing and feature extraction
- Model architecture design
- Dependencies: `requirements-model.txt`

### Phase 2: Training
- Model training pipeline
- Dataset processing
- Model evaluation and metrics
- Trained model storage
- Dependencies: `requirements-model.txt`

### Phase 3: Frontend
- Flask web application
- User interface implementation
- API endpoints
- Real-time prediction
- Dependencies: `requirements-web.txt`

### Phase 4: Documentation
- Project documentation
- Usage instructions
- API documentation
- Development guidelines

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ovijitM/spam_detect_with_NLP.git
cd spam_detect_with_NLP
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies based on your needs:
```bash
# For model development
pip install -r requirements-model.txt

# For web application
pip install -r requirements-web.txt

# For development
pip install -r requirements-dev.txt

# For all dependencies
pip install -r requirements.txt
```

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed information about the project organization.

## Usage

### Running the Web Application

1. Start the Flask application:
```bash
python src/web/app.py
```

2. Open your browser and navigate to `http://localhost:5000`

### Using the Model API

```python
from src.model.spam_filter import SpamFilter

# Load the trained model
model = SpamFilter.load_model('data/processed/spam_filter_model.pkl')

# Make predictions
prediction, probability = model.predict("Your message here")
print(f"Prediction: {prediction}, Confidence: {probability:.2%}")
```

## API Endpoints

### Check Spam
```bash
POST /check_spam
Content-Type: application/json

{
    "message": "Your message here"
}
```

Response:
```json
{
    "prediction": "spam/not_spam",
    "probability": 0.95,
    "is_spam": true/false
}
```

## Development

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation as needed
4. Use appropriate requirements file for each phase

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- SMS Spam Collection dataset
- Flask web framework
- scikit-learn and NLTK libraries 