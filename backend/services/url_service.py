import requests

def trace_redirects(url: str) -> dict:
    """Safely inspect redirects using requests with timeout."""
    info = {
        "redirect_count": 0,
        "final_url": url,
        "chain": [],
        "error": None
    }
    
    try:
        # Use a short timeout, and allow redirects up to a certain limit
        session = requests.Session()
        session.max_redirects = 5
        response = session.head(url, allow_redirects=True, timeout=3.0)
        
        info["final_url"] = response.url
        info["redirect_count"] = len(response.history)
        info["chain"] = [r.url for r in response.history] + [response.url]
        
    except requests.exceptions.TooManyRedirects:
        info["error"] = "Too many redirects."
    except requests.exceptions.RequestException as e:
        info["error"] = "Failed to reach URL."
        
    return info
