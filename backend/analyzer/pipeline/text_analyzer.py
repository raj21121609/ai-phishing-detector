import re

def analyze_text(body, subject=""):
    """Detects rule-based textual signals of phishing."""
    text_to_analyze = f"{subject} {body}".lower()
    
    signals = []
    
    patterns = {
        "urgency": r"\b(urgent|immediate|act now|action required|within \d+ hours|soon|asap)\b",
        "threats": r"\b(suspend|terminate|block|close your account|restrict|delete)\b",
        "password_request": r"\b(verify your account|confirm your password|update your password|reset password)\b",
        "credential_request": r"\b(login to|sign in to|click here to login|verify identity)\b",
        "payment_request": r"\b(invoice|payment overdue|transfer funds|bitcoin|btc|wallet|wire transfer)\b",
    }
    
    for signal_type, pattern in patterns.items():
        if re.search(pattern, text_to_analyze):
            signals.append(signal_type)
            
    return signals
