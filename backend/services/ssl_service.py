import ssl
import socket
from urllib.parse import urlparse

def get_ssl_info(url: str) -> dict:
    """Checks SSL certificate validity."""
    parsed = urlparse(url)
    if parsed.scheme != 'https':
        return {"valid": False, "error": "Not HTTPS"}
        
    hostname = parsed.hostname
    if not hostname:
        return {"valid": False, "error": "Invalid hostname"}
        
    context = ssl.create_default_context()
    context.check_hostname = False
    # Set a short timeout
    socket.setdefaulttimeout(3.0)
    
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return {"valid": True, "error": None}
    except Exception as e:
        return {"valid": False, "error": str(e)}
