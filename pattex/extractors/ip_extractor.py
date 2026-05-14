from pattex._utils._utils import (
    host_from_url,
)
from pattex.extractors.url_extractor import extract_urls

def _is_ip_host(url: str) -> bool:
    host = host_from_url(url)
    if not host:
        return False
    # IPv6 — urlparse strips brackets, so check original too
    if host.startswith("[") or ":" in host:
        return True
    # IPv4 — all 4 parts are digits
    parts = host.split(".")
    return len(parts) == 4 and all(p.isdigit() for p in parts)


def extract_ip_urls(
    text: str,
    ipv4: bool = True,
    ipv6: bool = True,
) -> list[str]:
    """
    Extract URLs whose host is an IP address.

    Args:
        text:  Input string to search.
        ipv4:  Include IPv4 URLs. Default True.
        ipv6:  Include IPv6 URLs. Default True.

    Returns:
        Deduplicated list of IP-based URL strings,
        with scheme lowercased and trailing noise stripped.
    """
    if not ipv4 and not ipv6:
        return []

    all_urls = extract_urls(text, mode="strict", allow_ipv4=ipv4, allow_ipv6=ipv6)

    return [
        url for url in all_urls
        if _is_ip_host(url)
        and (ipv4 if ":" not in host_from_url(url) else ipv6)
    ]