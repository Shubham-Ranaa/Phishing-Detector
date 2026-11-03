import re

def extract_urls(text: str) -> list[str]:
    """Extracts all URLs from a given text."""
    url_pattern = re.compile(
        r'(?:(?:https?|ftp)://)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
    )
    # Basic URL extraction, can be improved.
    urls = re.findall(r'(https?://[^\s]+)', text)
    # Try to find URLs without scheme
    urls_no_scheme = re.findall(r'(?<!://)\b([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)\b', text)
    
    all_urls = urls + [u if u.startswith('http') else 'http://' + u for u in urls_no_scheme]
    return list(set(all_urls))

def compute_string_similarity(s1: str, s2: str) -> float:
    """Computes similarity between two strings using Levenshtein distance concept simply."""
    if not s1 or not s2:
        return 0.0
    
    # A simple ratio for typo squatting without importing heavy libraries
    # Using Jaccard similarity of bigrams as a lightweight alternative
    def get_bigrams(string):
        s = string.lower()
        return set(s[i:i+2] for i in range(len(s)-1))
    
    b1 = get_bigrams(s1)
    b2 = get_bigrams(s2)
    if not b1 and not b2:
        return 1.0
    if not b1 or not b2:
        return 0.0
    
    intersection = len(b1.intersection(b2))
    union = len(b1.union(b2))
    return intersection / union
