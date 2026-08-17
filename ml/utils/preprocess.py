import re

def clean_text(text):
    """
    Cleans raw email text for machine learning.
    - Lowercases text
    - Removes URLs
    - Removes special characters and digits
    - Removes excessive whitespace
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
