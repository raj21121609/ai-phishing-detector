from .email_parser import parse_email
from .text_analyzer import analyze_text
from .url_extractor import extract_and_analyze_urls
from .sender_analyzer import analyze_sender

def analyze_email_content(raw_email_text):
    """Orchestrates the entire email analysis pipeline."""
    parsed_data = parse_email(raw_email_text)
    
    sender_signals = {}
    if parsed_data['sender']:
        sender_signals = analyze_sender(parsed_data['sender'], parsed_data.get('reply_to'))
        
    text_signals = analyze_text(parsed_data['body'], parsed_data.get('subject', ''))
    
    url_data = extract_and_analyze_urls(parsed_data['body'])
    
    return {
        "metadata": {
            "subject": parsed_data.get('subject'),
            "recipient": parsed_data.get('recipient'),
            "email_length": parsed_data.get('email_length')
        },
        "sender": sender_signals,
        "text_signals": text_signals,
        "urls": url_data,
        "url_signals": [] # Placeholder for aggregated URL signals if needed
    }
