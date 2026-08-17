import re
import difflib
from urllib.parse import urlparse

POPULAR_BRANDS = ['paypal', 'google', 'microsoft', 'apple', 'amazon', 'netflix', 'facebook', 'chase', 'bankofamerica']

def check_typosquatting(domain):
    """Detects obvious typosquatting attempts against popular brands."""
    domain_lower = domain.lower()
    base_domain = domain_lower.split('.')[0] if '.' in domain_lower else domain_lower
    
    for brand in POPULAR_BRANDS:
        if base_domain == brand:
            return None 
            
        similarity = difflib.SequenceMatcher(None, base_domain, brand).ratio()
        
        if 0.8 <= similarity < 1.0:
            return brand
            
        brand_regex = brand.replace('o', '[o0]').replace('l', '[l1i]').replace('e', '[e3]').replace('a', '[a@4]')
        if brand_regex != brand and re.fullmatch(brand_regex, base_domain):
            return brand
            
    return None

def analyze_url_security(url):
    """Analyzes a single URL and returns a risk score and signals."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
    except Exception:
        return {"url": url, "error": "Invalid URL format"}
        
    signals = []
    risk_score = 0
    
    # 1. URL Length
    url_length = len(url)
    if url_length > 100:
        signals.append("Abnormally long URL")
        risk_score += 15
        
    # 2. Domain Length
    domain_length = len(domain)
    if domain_length > 30:
        signals.append("Abnormally long domain name")
        risk_score += 10
        
    # 3. Subdomains
    parts = domain.split('.')
    subdomain_count = max(0, len(parts) - 2)
    if subdomain_count >= 2:
        signals.append(f"Multiple subdomains detected ({subdomain_count})")
        risk_score += 20
        
    # 4. HTTPS
    https_usage = (parsed.scheme == 'https')
    if not https_usage:
        signals.append("Unencrypted connection (HTTP)")
        risk_score += 15
        
    # 5. IP Address
    has_ip = bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain))
    if has_ip:
        signals.append("IP address used instead of domain name")
        risk_score += 40
        
    # 6. Suspicious Characters
    if '@' in url:
        signals.append("Contains '@' symbol (credential harvesting indicator)")
        risk_score += 30
    if domain.count('-') > 1:
        signals.append("Multiple dashes in domain")
        risk_score += 15
        
    # 7. Shortener
    shortener_domains = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly']
    is_shortened = any(short_dom in domain.lower() for short_dom in shortener_domains)
    if is_shortened:
        signals.append("URL shortener service used")
        risk_score += 25
        
    # 8. Keywords
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'auth', 'signin']
    found_keywords = [kw for kw in suspicious_keywords if kw in url.lower()]
    if found_keywords:
        signals.append(f"Suspicious keywords in URL: {', '.join(found_keywords)}")
        risk_score += min(30, len(found_keywords) * 15)
        
    # 9. Typosquatting
    impersonated_brand = check_typosquatting(domain)
    if impersonated_brand:
        signals.append(f"Possible brand impersonation of '{impersonated_brand}'")
        risk_score += 50
        
    risk_score = min(100, risk_score)
    
    return {
        "url": url,
        "risk_score": risk_score,
        "signals": signals,
        "features": {
            "url_length": url_length,
            "domain_length": domain_length,
            "subdomain_count": subdomain_count,
            "https_usage": https_usage,
            "has_ip": has_ip,
            "is_shortened": is_shortened,
            "suspicious_keywords": found_keywords,
            "impersonated_brand": impersonated_brand
        }
    }

def extract_and_analyze_urls(text):
    """Extracts URLs and runs security analysis on each."""
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*')
    urls = url_pattern.findall(text)
    
    analyzed_urls = []
    for url in set(urls):
        analysis = analyze_url_security(url)
        if "error" not in analysis:
            analyzed_urls.append(analysis)
            
    return analyzed_urls
