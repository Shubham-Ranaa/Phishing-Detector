from .rules import URGENCY_KEYWORDS, CREDENTIAL_KEYWORDS, FINANCIAL_KEYWORDS, REWARD_KEYWORDS, THREAT_KEYWORDS
from .utils import extract_urls
from .scoring import calculate_risk_score, generate_recommendations
from .url_detector import analyze_url

def analyze_message(message: str) -> dict:
    msg_lower = message.lower()
    checks = []
    
    # Check Urgency
    if any(kw in msg_lower for kw in URGENCY_KEYWORDS):
        checks.append({
            "id": "urgency",
            "title": "Urgent Language",
            "status": "WARNING",
            "explanation": "Message contains urgent language, often used to create panic.",
            "score_impact": 10
        })
        
    # Check Credentials
    if any(kw in msg_lower for kw in CREDENTIAL_KEYWORDS):
        checks.append({
            "id": "credential_request",
            "title": "Credential Request",
            "status": "DANGER",
            "explanation": "Message asks for sensitive credentials (e.g. password, OTP).",
            "score_impact": 25
        })
        
    # Check Financial
    if any(kw in msg_lower for kw in FINANCIAL_KEYWORDS):
        checks.append({
            "id": "financial_request",
            "title": "Financial Request",
            "status": "WARNING",
            "explanation": "Message discusses payment, bank transfer, or crypto.",
            "score_impact": 20
        })
        
    # Check Rewards
    if any(kw in msg_lower for kw in REWARD_KEYWORDS):
        checks.append({
            "id": "reward",
            "title": "Unexpected Reward",
            "status": "WARNING",
            "explanation": "Promises unexpected rewards or prizes (common in scams).",
            "score_impact": 15
        })
        
    # Check Threats
    if any(kw in msg_lower for kw in THREAT_KEYWORDS):
        checks.append({
            "id": "threat",
            "title": "Threatening Language",
            "status": "DANGER",
            "explanation": "Threatens account closure or legal action to force compliance.",
            "score_impact": 15
        })
        
    # Check URLs
    urls = extract_urls(message)
    if urls:
        checks.append({
            "id": "contains_url",
            "title": f"Contains {len(urls)} URL(s)",
            "status": "INFO",
            "explanation": "Message contains embedded links.",
            "score_impact": 10
        })
        
        # Analyze first URL if present
        first_url = urls[0]
        try:
            url_res = analyze_url(first_url)
            if url_res["risk_score"] > 24:
                checks.append({
                    "id": "suspicious_url_embedded",
                    "title": "Suspicious URL Embedded",
                    "status": "DANGER",
                    "explanation": f"Embedded URL ({first_url}) was flagged as suspicious.",
                    "score_impact": 20
                })
        except Exception:
            pass
            
    if not checks:
        checks.append({
            "id": "clean_message",
            "title": "No Obvious Threats",
            "status": "PASS",
            "explanation": "No common scam keywords or malicious URLs detected.",
            "score_impact": 0
        })

    score, threat_level = calculate_risk_score(checks)
    recommendations = generate_recommendations(score, checks)
    
    return {
        "status": threat_level.lower().replace(" ", "_"),
        "risk_score": score,
        "threat_level": threat_level,
        "confidence": "Medium",
        "summary": f"This message scored {score}. Found {len(checks)} potential indicators.",
        "checks": checks,
        "recommendations": recommendations
    }
