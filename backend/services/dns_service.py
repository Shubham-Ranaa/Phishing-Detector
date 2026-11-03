import dns.resolver
import socket

def get_domain_info(domain: str) -> dict:
    """Attempts to get A records for the domain."""
    info = {
        "resolved_ip": None,
        "error": None
    }
    
    # Remove port if exists
    domain = domain.split(':')[0]
    
    try:
        answers = dns.resolver.resolve(domain, 'A')
        ips = [rdata.address for rdata in answers]
        if ips:
            info['resolved_ip'] = ips[0]
    except Exception as e:
        # Fallback to simple resolution
        try:
            ip = socket.gethostbyname(domain)
            info['resolved_ip'] = ip
        except Exception as e2:
            info['error'] = "Domain information unavailable."
            
    return info
