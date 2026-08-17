import os
import sys
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocess import clean_text

class PhishingClassifier:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'model.joblib')
        vectorizer_path = os.path.join(base_dir, 'models', 'vectorizer.joblib')
        
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.is_loaded = True
        except Exception as e:
            print(f"Warning: Could not load ML artifacts. {e}")
            self.is_loaded = False

    def predict(self, email_text):
        if not self.is_loaded:
            return {"prediction": "unknown", "probability": 0.0, "error": "Model not loaded"}
            
        cleaned = clean_text(email_text)
        if not cleaned:
            return {"prediction": "legitimate", "probability": 0.0}
            
        vectorized = self.vectorizer.transform([cleaned])
        
        probs = self.model.predict_proba(vectorized)[0]
        prob_phishing = float(probs[1])
        
        prediction = "phishing" if prob_phishing >= 0.5 else "legitimate"
        
        return {
            "prediction": prediction,
            "probability": round(prob_phishing, 4)
        }

_classifier = None

def predict_email(email_text):
    global _classifier
    if _classifier is None:
        _classifier = PhishingClassifier()
    return _classifier.predict(email_text)
