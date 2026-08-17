# PhishGuard AI

## 1. Project Overview
PhishGuard AI is an advanced, AI-powered email threat detection web application designed to identify and explain phishing attempts in real-time. It provides a user-friendly interface for pasting suspicious emails and instantly visualizes the threat landscape through a dynamic risk engine.

## 2. Problem Statement
Phishing attacks are becoming increasingly sophisticated, blending legitimate formatting with malicious intent. Traditional rule-based filters often fail to catch zero-day attacks, while pure machine learning solutions act as "black boxes" that fail to explain *why* an email is dangerous. PhishGuard AI bridges this gap by combining modular heuristics, typosquatting detection, and machine learning into an Explainable AI (XAI) pipeline.

## 3. Features
- **Multi-layered Analysis**: Extracts and analyzes sender details, embedded URLs, and text sentiment.
- **Machine Learning**: Utilizes NLP and TF-IDF vectorization to classify patterns.
- **Risk Scoring Engine**: Computes a granular 0-100 risk score based on configured heuristic and ML weights.
- **Explainability Engine**: Translates raw data into human-readable threat cards and recommendations.
- **Privacy-First History**: Persists analysis metadata and threat reports without permanently storing raw email bodies.
- **Interactive UI**: A modern, responsive React dashboard showcasing threats with distinct visual severity indicators.

## 4. Architecture
The system follows a decoupled architecture:
- **Frontend (React)**: Handles user input, state management, and renders the `ResultsDisplay` component.
- **Backend API (Django REST)**: An orchestration pipeline that sequentially parses the email, runs isolated analyzer modules (`sender_analyzer`, `url_extractor`, `text_analyzer`), queries the ML model, and aggregates everything in the `risk_engine` and `explainer`.
- **ML Pipeline (Python/Scikit-Learn)**: A standalone environment for dataset parsing, TF-IDF vectorization, model training, and `.joblib` serialization.

## 5. Tech Stack
- **Frontend**: React 18, Vite, Tailwind CSS, Axios, React Router.
- **Backend**: Python 3, Django, Django REST Framework.
- **Database**: SQLite (Development) / Ready for PostgreSQL (Production).
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib.

## 6. ML Methodology
The ML pipeline frames phishing detection as a binary classification problem (0 = Legitimate, 1 = Phishing). 
1. **Preprocessing**: URLs, special characters, and digits are stripped to isolate semantic text.
2. **Vectorization**: Term Frequency-Inverse Document Frequency (TF-IDF) is used to convert textual features into numerical vectors.
3. **Model**: A Logistic Regression classifier, chosen for its fast inference speed, interpretability, and strong baseline performance on text classification.

## 7. Dataset
The model was initially trained on a proprietary dummy dataset designed to bootstrap the pipeline. The dataset contains labeled columns for `text` and `label` (0 or 1). The pipeline is fully configured to retrain seamlessly when a larger production `.csv` dataset is provided to `ml/datasets/`.

## 8. Model Evaluation
The current baseline model achieves perfect evaluation metrics (1.0 Precision, 1.0 Recall, 1.0 F1-Score) on the small bootstrap dataset. The training pipeline exports a confusion matrix and these classification metrics during every training run to ensure quality control as the dataset grows.

## 9. API Documentation
**`POST /api/analyze/`**
- **Payload**: `{"email_text": "..."}`
- **Response**: Returns a structured JSON containing `risk_score`, `risk_level`, `phishing_probability`, `email` metadata, `url_analysis` array, `threats` array, and an `explanation` object.

**`GET /api/history/`**
- **Response**: Returns a paginated list of previously analyzed records (excluding raw analysis data for speed).

**`GET /api/history/<uuid>/`**
- **Response**: Returns a specific historical record including the full `analysis_data` payload to reconstruct the UI.

## 10. Installation
1. Clone the repository.
2. **Backend**: Navigate to `backend/`, create a virtual environment, and run `pip install -r requirements.txt`.
3. **Frontend**: Navigate to `frontend/` and run `npm install`.

## 11. Environment Variables
Create a `.env` file in the `backend/` directory:
```
SECRET_KEY=your_secure_random_key
DEBUG=True
CORS_ALLOWED_ORIGINS=http://localhost:3000
DATABASE_URL=sqlite:///db.sqlite3
```
Create a `.env` file in the `frontend/` directory:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## 12. Running Locally
1. Start the Django backend: `python manage.py runserver 8000`
2. Start the React frontend: `npm run dev`
3. (Optional) Retrain the ML model: `cd ml && python training/train.py`

## 13. Security Considerations
- **Privacy**: Raw email bodies are deliberately NOT saved to the database to protect user privacy.
- **Input Validation**: The API enforces a strict 100,000-character limit to prevent DoS attacks.
- **Rate Limiting**: Configured at 100 requests/day for anonymous users.
- **Safe Headers**: `SECURE_BROWSER_XSS_FILTER` and `X_FRAME_OPTIONS` are enabled.
- **Exception Handling**: The orchestrator is wrapped in a protective `try/except` block to guarantee internal stack traces are never leaked in 500 errors.

## 14. Limitations
- The current ML model is trained on a small bootstrap dataset; production deployment requires training on a larger corpus of phishing emails (e.g., the Enron corpus).
- URL analysis is entirely heuristic and does not perform active web crawling or DNS lookups to avoid triggering alarms or accessing malicious code.

## 15. Future Scope
- **Active URL Scanning**: Integrate with APIs like VirusTotal or Google Safe Browsing.
- **Advanced NLP**: Upgrade the Logistic Regression model to a Transformer architecture (e.g., BERT) for deeper contextual understanding.
- **Browser Extension**: Build a Chrome extension to inject the PhishGuard analysis directly into Gmail or Outlook interfaces.
