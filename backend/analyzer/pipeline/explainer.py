def generate_explanation(risk_level, risk_score, ml_probability, details):
    """
    Generates structured explainability output based on raw signals.
    Returns: { "summary": str, "reasons": list, "recommendation": str }
    """
    reasons = []
    
    # 1. ML Signal
    if ml_probability >= 0.8:
        reasons.append({
            "severity": "HIGH",
            "category": "MACHINE_LEARNING",
            "message": "Our AI model confidently classified the overall pattern of this email as malicious."
        })
    elif ml_probability >= 0.6:
        reasons.append({
            "severity": "MEDIUM",
            "category": "MACHINE_LEARNING",
            "message": "Our AI model flagged suspicious patterns in the email text."
        })

    # 2. URL Signals
    url_data = details.get("urls", [])
    for u in url_data:
        features = u.get("features", {})
        if features.get("impersonated_brand"):
            brand = features["impersonated_brand"]
            reasons.append({
                "severity": "HIGH",
                "category": "URL",
                "message": f"The URL attempts to impersonate the brand '{brand}'."
            })
        if features.get("has_ip"):
            reasons.append({
                "severity": "HIGH",
                "category": "URL",
                "message": "A URL uses a raw IP address instead of a standard domain name to hide its destination."
            })
        if features.get("is_shortened"):
            reasons.append({
                "severity": "MEDIUM",
                "category": "URL",
                "message": "A URL shortening service is used, which often obscures malicious links."
            })

    # 3. Sender Signals
    sender_data = details.get("sender", {})
    if sender_data.get("reply_to_mismatch"):
        reasons.append({
            "severity": "HIGH",
            "category": "SENDER",
            "message": "The 'Reply-To' address differs from the 'From' address, a common spoofing tactic."
        })
    if sender_data.get("suspicious_domain_structure"):
        reasons.append({
            "severity": "MEDIUM",
            "category": "SENDER",
            "message": "The sender's domain has an overly complex or suspicious structure."
        })

    # 4. Text/Social Engineering Signals
    text_signals = details.get("text_signals", [])
    if "urgency" in text_signals:
        reasons.append({
            "severity": "MEDIUM",
            "category": "SOCIAL_ENGINEERING",
            "message": "The email uses urgent language to pressure you into acting quickly."
        })
    if "threats" in text_signals:
        reasons.append({
            "severity": "HIGH",
            "category": "SOCIAL_ENGINEERING",
            "message": "The email threatens negative consequences (like account suspension) to force compliance."
        })
    if "password_request" in text_signals or "credential_request" in text_signals:
        reasons.append({
            "severity": "HIGH",
            "category": "SOCIAL_ENGINEERING",
            "message": "The email asks you to verify or provide sensitive account credentials."
        })
    if "payment_request" in text_signals:
        reasons.append({
            "severity": "MEDIUM",
            "category": "SOCIAL_ENGINEERING",
            "message": "The email requests payment or financial transfers."
        })
        
    # Deduplicate reasons
    seen = set()
    unique_reasons = []
    for r in reasons:
        if r["message"] not in seen:
            unique_reasons.append(r)
            seen.add(r["message"])

    # Generate Summary and Recommendation
    if risk_level == "CRITICAL" or risk_level == "HIGH":
        summary = "This email shows strong characteristics commonly associated with phishing or malicious activity."
        recommendation = "Do not click any links or download attachments. Report this email to your security team and delete it immediately."
    elif risk_level == "MEDIUM":
        summary = "This email contains suspicious elements and warrants caution."
        recommendation = "Avoid interacting with the links. If this is a known sender, verify their request via a separate, trusted channel."
    else:
        if not unique_reasons:
            summary = "No significant threats or suspicious patterns were detected in this email."
            recommendation = "The email appears safe, but always remain vigilant and verify unexpected requests."
        else:
            summary = "The email appears mostly safe, but contains some minor anomalies."
            recommendation = "Standard caution is advised. Verify links before clicking."

    return {
        "summary": summary,
        "reasons": unique_reasons,
        "recommendation": recommendation
    }
