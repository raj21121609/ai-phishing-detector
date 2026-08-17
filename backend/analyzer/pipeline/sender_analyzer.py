import re

def analyze_sender(sender, reply_to=None):
    """Analyzes the sender and reply-to email addresses."""
    if not sender:
        return {"error": "No sender provided"}
        
    sender_domain = ""
    sender_email = ""
    
    email_match = re.search(r'<([^>]+)>', sender)
    if email_match:
        sender_email = email_match.group(1).lower()
    else:
        sender_email = sender.lower()
        
    if '@' in sender_email:
        sender_domain = sender_email.split('@')[1]
        
    free_providers = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
    is_free_provider = sender_domain in free_providers
    
    reply_to_mismatch = False
    if reply_to:
        rt_match = re.search(r'<([^>]+)>', reply_to)
        rt_email = rt_match.group(1).lower() if rt_match else reply_to.lower()
        if rt_email and rt_email != sender_email:
            reply_to_mismatch = True
            
    suspicious_structure = False
    if sender_domain:
        if sender_domain.count('-') > 2 or len(sender_domain) > 40:
            suspicious_structure = True
            
    return {
        "sender_email": sender_email,
        "sender_domain": sender_domain,
        "is_free_provider": is_free_provider,
        "reply_to_mismatch": reply_to_mismatch,
        "suspicious_domain_structure": suspicious_structure
    }
