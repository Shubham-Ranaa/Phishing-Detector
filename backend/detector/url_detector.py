import re
from urllib.parse import urlparse, unquote
import tldextract

from .rules import SUSPICIOUS_KEYWORDS, SUSPICIOUS_TLDS, KNOWN_BRANDS, URL_SHORTENERS
from .utils import compute_string_similarity
from .scoring import calculate_risk_score, generate_recommendations
from services.dns_service import get_domain_info
from services.ssl_service import get_ssl_info
from services.url_service import trace_redirects

def analyze_url(url: str) -> dict:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    parsed_url = urlparse(url)
    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}"
    
    checks = []
    
    # 1. HTTPS Check
    if parsed_url.scheme == 'http':
        checks.append({
            "id": "https",
            "title": "Unencrypted Connection",
            "status": "WARNING",
            "explanation": "This URL uses HTTP. Data sent over this connection is unencrypted.",
            "score_impact": 10
        })
    else:
        checks.append({
            "id": "https",
            "title": "HTTPS Connection",
            "status": "PASS",
            "explanation": "Secure HTTPS connection detected.",
            "score_impact": 0
        })

    # 2. IP Address Check
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if ip_pattern.match(parsed_url.hostname or ""):
        checks.append({
            "id": "ip_domain",
            "title": "Direct IP Address",
            "status": "DANGER",
            "explanation": "URL uses an IP address directly instead of a domain name.",
            "score_impact": 20
        })
        
    # 3. URL Length
    if len(url) > 75:
        checks.append({
            "id": "url_length",
            "title": "URL Length",
            "status": "WARNING",
            "explanation": "URL is unusually long, which can be used to hide suspicious parameters.",
            "score_impact": 10
        })
        
    # 4. @ Symbol Check
    if '@' in parsed_url.netloc:
        checks.append({
            "id": "at_symbol",
            "title": "Authentication Symbol (@)",
            "status": "DANGER",
            "explanation": "URL contains an @ symbol, often used to obscure the true destination.",
            "score_impact": 25
        })
        
    # 5. Suspicious Keywords
    path_and_query = (parsed_url.path + parsed_url.query).lower()
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in path_and_query or kw in domain]
    if found_keywords:
        checks.append({
            "id": "suspicious_keywords",
            "title": "Suspicious Keywords",
            "status": "WARNING",
            "explanation": f"URL contains keywords commonly used in phishing: {', '.join(found_keywords)}",
            "score_impact": 5 * min(len(found_keywords), 3) # Max +15
        })
        
    # 6. Suspicious TLD
    if f".{ext.suffix}" in SUSPICIOUS_TLDS:
        checks.append({
            "id": "suspicious_tld",
            "title": "Suspicious TLD",
            "status": "WARNING",
            "explanation": f"The top-level domain (.{ext.suffix}) is frequently used by malicious sites.",
            "score_impact": 10
        })
        
    # 7. Excessive Subdomains
    subdomains = ext.subdomain.split('.') if ext.subdomain else []
    if len(subdomains) > 2:
        checks.append({
            "id": "excessive_subdomains",
            "title": "Excessive Subdomains",
            "status": "WARNING",
            "explanation": "Domain structure is unusually complex with multiple subdomains.",
            "score_impact": 10
        })
        
    # 8. Suspicious Characters
    if '-' * 3 in domain or url.startswith('xn--'):
        checks.append({
            "id": "suspicious_chars",
            "title": "Suspicious Characters",
            "status": "WARNING",
            "explanation": "Domain contains excessive hyphens or punycode, common in evasion tactics.",
            "score_impact": 15
        })

    # 9. Typosquatting
    is_typo = False
    for brand in KNOWN_BRANDS:
        if domain == brand:
            break # Exact match
        sim = compute_string_similarity(domain, brand)
        if 0.7 < sim < 1.0: # high similarity but not exact
            checks.append({
                "id": "typosquatting",
                "title": "Typosquatting Detected",
                "status": "DANGER",
                "explanation": f"Domain resembles known brand '{brand}' and may be attempting impersonation.",
                "score_impact": 25
            })
            is_typo = True
            break
            
    # 10. Domain Info
    if parsed_url.hostname and not ip_pattern.match(parsed_url.hostname):
        dns_info = get_domain_info(parsed_url.hostname)
        if dns_info.get("resolved_ip"):
            checks.append({
                "id": "dns",
                "title": "Domain Resolution",
                "status": "INFO",
                "explanation": f"Domain resolves to IP {dns_info['resolved_ip']}.",
                "score_impact": 0
            })
        else:
            checks.append({
                "id": "dns",
                "title": "Domain Resolution Failed",
                "status": "WARNING",
                "explanation": "Domain information unavailable.",
                "score_impact": 5
            })

    # 11. SSL Certificate
    if parsed_url.scheme == 'https':
        ssl_info = get_ssl_info(url)
        if ssl_info.get("valid"):
            checks.append({
                "id": "ssl",
                "title": "SSL Certificate",
                "status": "PASS",
                "explanation": "Certificate appears valid.",
                "score_impact": 0
            })
        else:
            checks.append({
                "id": "ssl",
                "title": "SSL Certificate Issue",
                "status": "WARNING",
                "explanation": "Could not verify SSL certificate.",
                "score_impact": 10
            })

    # 12. Redirect Analysis
    redirect_info = trace_redirects(url)
    if redirect_info.get("redirect_count", 0) > 2:
        checks.append({
            "id": "redirects",
            "title": "Multiple Redirects",
            "status": "WARNING",
            "explanation": f"URL redirects {redirect_info['redirect_count']} times, hiding final destination.",
            "score_impact": 15
        })

    # 13. URL Shorteners
    if domain in URL_SHORTENERS:
        checks.append({
            "id": "shortener",
            "title": "URL Shortener",
            "status": "INFO",
            "explanation": "Shortened URL — destination is hidden.",
            "score_impact": 5
        })

    # 14. Suspicious Domain Patterns (Combined logic)
    brand_word_in_domain = any(b.split('.')[0] in domain for b in KNOWN_BRANDS)
    security_word_in_domain = any(kw in domain for kw in ["secure", "login", "update", "verify"])
    if brand_word_in_domain and security_word_in_domain and not is_typo:
        checks.append({
            "id": "suspicious_pattern",
            "title": "Suspicious Domain Pattern",
            "status": "DANGER",
            "explanation": "Domain combines a brand name with security keywords (e.g. secure-login).",
            "score_impact": 20
        })

    score, threat_level = calculate_risk_score(checks)
    recommendations = generate_recommendations(score, checks)

    # Clean checks to ensure UI compatibility
    # Ensure PASS/INFO/WARNING/DANGER statuses
    
    return {
        "status": threat_level.lower().replace(" ", "_"), # 'safe', 'low_risk', 'suspicious', 'high_risk'
        "risk_score": score,
        "threat_level": threat_level,
        "confidence": "High",
        "summary": f"This URL has a risk score of {score}. {len([c for c in checks if c['status'] in ['WARNING', 'DANGER']])} suspicious flags detected.",
        "checks": checks,
        "recommendations": recommendations
    }
