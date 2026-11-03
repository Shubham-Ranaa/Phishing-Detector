from .rules import KNOWN_BRANDS
from .message_detector import analyze_message

def analyze_email(sender: str, subject: str, body: str) -> dict:
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    
    # Treat the email as a combined message for base analysis
    combined_message = f"{subject}\n{body}"
    base_result = analyze_message(combined_message)
    checks = base_result.get("checks", [])
    
    # Add email-specific checks
    
    # 1. Free Email Provider Impersonation
    free_providers = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@aol.com"]
    is_free_provider = any(sender_lower.endswith(fp) for fp in free_providers)
    
    impersonating_brand = None
    for brand in KNOWN_BRANDS:
        brand_name = brand.split('.')[0]
        if brand_name in sender_lower or brand_name in subject_lower:
            impersonating_brand = brand_name
            break
            
    if is_free_provider and impersonating_brand:
        checks.append({
            "id": "free_email_impersonation",
            "title": "Suspicious Sender Address",
            "status": "DANGER",
            "explanation": f"Sender uses a free email provider but claims to represent {impersonating_brand}.",
            "score_impact": 25
        })
        
    # 2. Suspicious Subject Line
    if "urgent" in subject_lower or "action required" in subject_lower:
        checks.append({
            "id": "urgent_subject",
            "title": "Urgent Subject Line",
            "status": "WARNING",
            "explanation": "Subject line uses urgency to force immediate action.",
            "score_impact": 10
        })

    from .scoring import calculate_risk_score, generate_recommendations
    score, threat_level = calculate_risk_score(checks)
    recommendations = generate_recommendations(score, checks)
    
    if score >= 75:
        recommendations.append("Do not reply to this email.")

    return {
        "status": threat_level.lower().replace(" ", "_"),
        "risk_score": score,
        "threat_level": threat_level,
        "confidence": "Medium",
        "summary": f"This email scored {score}. Found {len(checks)} potential indicators.",
        "checks": checks,
        "recommendations": recommendations
    }
