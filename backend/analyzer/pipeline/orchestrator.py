import sys
import os

from .email_parser import parse_email
from .text_analyzer import analyze_text
from .url_extractor import extract_and_analyze_urls
from .sender_analyzer import analyze_sender
from .risk_engine import calculate_risk_score

ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ml'))
if ml_path not in sys.path:
    sys.path.append(ml_path)

from inference.predict import predict_email

def analyze_email_content(raw_email_text):
    """Orchestrates the entire email analysis pipeline."""
    parsed_data = parse_email(raw_email_text)
    
    sender_signals = {}
    if parsed_data['sender']:
        sender_signals = analyze_sender(parsed_data['sender'], parsed_data.get('reply_to'))
        
    text_signals = analyze_text(parsed_data['body'], parsed_data.get('subject', ''))
    
    url_data = extract_and_analyze_urls(parsed_data['body'])
    
    text_for_ml = f"{parsed_data.get('subject', '')} {parsed_data.get('body', '')}".strip()
    ml_data = predict_email(text_for_ml)
    
    risk_results = calculate_risk_score(ml_data, text_signals, url_data, sender_signals)
    
    return {
        "risk_score": risk_results["risk_score"],
        "risk_level": risk_results["risk_level"],
        "ml_probability": ml_data.get("probability", 0.0),
        "detected_threats": risk_results["detected_threats"],
        "metadata": {
            "subject": parsed_data.get('subject'),
            "recipient": parsed_data.get('recipient'),
            "email_length": parsed_data.get('email_length')
        },
        "details": {
            "sender": sender_signals,
            "text_signals": text_signals,
            "urls": url_data
        }
    }
