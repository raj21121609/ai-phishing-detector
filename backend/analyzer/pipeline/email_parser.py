import email
from email.policy import default

def parse_email(raw_text):
    """Parses raw email text into structured components."""
    # Try to parse as RFC 822 email
    msg = email.message_from_string(raw_text, policy=default)
    
    sender = msg.get('From', '')
    recipient = msg.get('To', '')
    subject = msg.get('Subject', '')
    reply_to = msg.get('Reply-To', '')
    
    # Extract body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body += part.get_payload(decode=True).decode()
                except:
                    body += part.get_payload()
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            body = msg.get_payload()
            
    # Fallback: if no headers found, treat entire text as body
    if not sender and not subject and not recipient:
        body = raw_text

    return {
        "sender": sender.strip() if sender else None,
        "recipient": recipient.strip() if recipient else None,
        "subject": subject.strip() if subject else None,
        "reply_to": reply_to.strip() if reply_to else None,
        "body": body.strip(),
        "email_length": len(raw_text)
    }
