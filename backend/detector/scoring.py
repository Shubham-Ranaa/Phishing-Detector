def calculate_risk_score(checks: list[dict]) -> tuple[int, str]:
    """
    Calculates the final risk score based on the list of checks.
    Each check should have a 'score_impact' (int).
    Returns (score, threat_level).
    """
    score = 0
    for check in checks:
        if 'score_impact' in check:
            score += check['score_impact']
    
    # Cap score at 100 and min 0
    score = max(0, min(100, score))
    
    # Determine Threat Level
    # 0–24     SAFE
    # 25–49    LOW RISK
    # 50–74    SUSPICIOUS
    # 75–100   HIGH RISK
    
    if score <= 24:
        threat_level = "SAFE"
    elif score <= 49:
        threat_level = "LOW RISK"
    elif score <= 74:
        threat_level = "SUSPICIOUS"
    else:
        threat_level = "HIGH RISK"
        
    return score, threat_level

def generate_recommendations(score: int, checks: list[dict]) -> list[str]:
    recommendations = set()
    
    if score >= 75:
        recommendations.add("Do not enter your password.")
        recommendations.add("Do not provide payment information.")
        recommendations.add("Avoid downloading files from this source.")
    
    has_typosquat = any(c.get('id') == 'typosquatting' and c.get('status') in ['WARNING', 'DANGER'] for c in checks)
    if has_typosquat:
        recommendations.add("Open the official website manually instead of clicking the link.")
        
    has_credential_req = any(c.get('id') == 'credential_request' for c in checks)
    if has_credential_req:
        recommendations.add("Verify the sender before taking action.")
        
    if score < 25:
        recommendations.add("This seems safe, but always remain vigilant.")
        
    return list(recommendations)
