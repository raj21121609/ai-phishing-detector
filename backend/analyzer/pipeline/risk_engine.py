def calculate_risk_score(ml_data, text_signals, url_data, sender_data):
    """
    Calculates the final risk score based on configured weights.
    Returns: { "risk_score": 0-100, "risk_level": "...", "detected_threats": [...] }
    """
    weights = {
        "ml": 40,
        "url": 30,
        "sender": 15,
        "text": 15
    }
    
    score = 0
    threats = set()
    
    # 1. ML Probability
    ml_prob = ml_data.get('probability', 0.0)
    score += (ml_prob * weights["ml"])
    
    if ml_prob >= 0.8:
        threats.add("High confidence machine learning phishing detection")
    elif ml_prob >= 0.6:
        threats.add("Suspicious machine learning classification")
        
    # 2. URL Analysis
    max_url_risk = 0
    for u in url_data:
        risk = u.get("risk_score", 0)
        max_url_risk = max(max_url_risk, risk)
        for sig in u.get("signals", []):
            threats.add(sig)
            
    score += (max_url_risk / 100.0) * weights["url"]
    
    # 3. Sender Analysis
    sender_risk = 0
    if sender_data.get("reply_to_mismatch"):
        sender_risk += 50
        threats.add("Sender and Reply-To addresses do not match")
    if sender_data.get("suspicious_domain_structure"):
        sender_risk += 30
        threats.add("Suspicious sender domain structure")
    if sender_data.get("is_free_provider"):
        sender_risk += 20
        
    score += (min(100, sender_risk) / 100.0) * weights["sender"]
    
    # 4. Text/Social Engineering
    text_risk = 0
    text_points = {
        "urgency": 30,
        "threats": 50,
        "password_request": 60,
        "credential_request": 50,
        "payment_request": 40
    }
    
    for sig in text_signals:
        text_risk += text_points.get(sig, 0)
        threats.add(f"Textual indicator: {sig.replace('_', ' ')}")
        
    score += (min(100, text_risk) / 100.0) * weights["text"]
    
    final_score = int(min(100, round(score)))
    
    if final_score >= 80:
        level = "CRITICAL"
    elif final_score >= 60:
        level = "HIGH"
    elif final_score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"
        
    return {
        "risk_score": final_score,
        "risk_level": level,
        "detected_threats": sorted(list(threats))
    }
