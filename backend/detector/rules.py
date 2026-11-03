# Configuration for rules and keywords

SUSPICIOUS_KEYWORDS = [
    "login", "signin", "verify", "verification", "account", "secure", 
    "security", "update", "password", "wallet", "bank", "banking", 
    "payment", "confirm", "recover", "unlock", "urgent", "claim", 
    "refund", "bonus", "prize", "gift", "free", "crypto", "support"
]

SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".click", ".work", ".shop", ".tk", ".ml", ".ga", ".cf"
]

KNOWN_BRANDS = [
    "google.com", "paypal.com", "microsoft.com", "apple.com", "amazon.com",
    "facebook.com", "instagram.com", "netflix.com", "linkedin.com", "github.com"
]

URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly", "cutt.ly"
]

# Message/Email specific rules
URGENCY_KEYWORDS = [
    "urgent", "immediately", "act now", "within 24 hours", "last warning", 
    "final notice", "asap", "action required"
]

CREDENTIAL_KEYWORDS = [
    "password", "otp", "pin", "cvv", "verification code", "login", "username", "passcode"
]

FINANCIAL_KEYWORDS = [
    "bank", "payment", "refund", "transfer", "money", "upi", "crypto", "wallet", "invoice"
]

REWARD_KEYWORDS = [
    "winner", "prize", "lottery", "gift", "free", "congratulations", "claim", "reward"
]

THREAT_KEYWORDS = [
    "account suspended", "account blocked", "legal action", "police", "fine", "penalty", "terminate"
]
