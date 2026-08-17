import re
from urllib.parse import urlparse

def extract_and_analyze_urls(text):
    """Extracts URLs and calculates features for each."""
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*')
    urls = url_pattern.findall(text)
    
    analyzed_urls = []
    shortener_domains = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd']
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking']
    
    for url in set(urls):
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            subdomain_count = max(0, len(domain.split('.')) - 2)
            has_ip = bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain))
            is_shortened = any(short_dom in domain.lower() for short_dom in shortener_domains)
            
            has_at_symbol = '@' in url
            has_dash_in_domain = '-' in domain
            
            found_keywords = [kw for kw in suspicious_keywords if kw in url.lower()]
            
            analyzed_urls.append({
                "url": url,
                "domain": domain,
                "url_length": len(url),
                "https_usage": parsed.scheme == 'https',
                "subdomain_count": subdomain_count,
                "has_ip": has_ip,
                "is_shortened": is_shortened,
                "suspicious_characters": {
                    "at_symbol": has_at_symbol,
                    "dash_in_domain": has_dash_in_domain
                },
                "suspicious_keywords": found_keywords
            })
        except Exception:
            continue
            
    return analyzed_urls
