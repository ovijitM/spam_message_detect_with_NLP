# Spam Detection with NLP - Vercel Deployment

This project is now configured for deployment on Vercel!

## 🚀 Deploy to Vercel

### Option 1: Deploy via Vercel CLI
1. Install Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```

2. Login to your Vercel account:
   ```bash
   vercel login
   ```

3. Deploy from the project root:
   ```bash
   vercel
   ```

### Option 2: Deploy via GitHub Integration
1. Push your code to a GitHub repository
2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your GitHub repository
5. Vercel will automatically detect the configuration and deploy

## 📁 Project Structure for Vercel

```
spam_detect_with_NLP/
├── api/
│   └── index.py          # Main Flask application for Vercel
├── vercel.json           # Vercel configuration
├── requirements-vercel.txt # Python dependencies for Vercel
└── ... (other files)
```

## ⚙️ Configuration Files

- **vercel.json**: Configures Vercel to serve the Flask app
- **api/index.py**: Self-contained Flask application with embedded HTML and ML model
- **requirements-vercel.txt**: Dependencies for Vercel deployment

## 🔧 How it Works

1. **Serverless Functions**: The app runs as a serverless function on Vercel
2. **Embedded Model**: Uses a lightweight training dataset since file system access is limited
3. **Single File**: Everything is contained in `api/index.py` for simplicity
4. **Auto-scaling**: Vercel automatically scales based on traffic

## 🌐 After Deployment

Once deployed, you'll get a URL like:
- `https://your-project-name.vercel.app/`

The spam detection API will be available at:
- `https://your-project-name.vercel.app/api/check_spam`

## 📝 Environment Variables (Optional)

If you need to add environment variables:
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add your variables

## 🔍 Features

- ✅ Responsive web interface
- ✅ Real-time spam detection
- ✅ Confidence scoring
- ✅ Beautiful gradient UI
- ✅ Error handling
- ✅ Loading states

## 🛠️ Local Development

To test locally before deploying:
```bash
cd api
python index.py
```

Visit `http://localhost:5000` to test the application.

## 📊 Model Details

**🚀 OPTIMIZED FOR VERCEL - NO SIZE LIMITS!**

The deployment uses a custom lightweight Naive Bayes implementation:
- **No Heavy Dependencies**: Custom ML implementation (no scikit-learn, pandas, or nltk)
- **Tiny Size**: Only Flask required (~5MB vs 250MB+ with ML libraries)
- **Fast Performance**: Quick cold starts and efficient processing
- **Production Ready**: Includes Laplace smoothing and proper probability calculations

### Technical Improvements:
- ✅ Removed scikit-learn, pandas, nltk dependencies
- ✅ Custom Naive Bayes with Laplace smoothing
- ✅ Built-in stop words list (no external downloads)
- ✅ Optimized for serverless deployment
- ✅ Under 50MB total size (well within Vercel's limits)

For production use, you can easily extend this by:
- Adding more training data to the built-in dataset
- Implementing more sophisticated text preprocessing
- Adding custom feature engineering

Enjoy your spam detection app on Vercel! 🎉
