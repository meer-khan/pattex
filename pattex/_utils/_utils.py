import re
from urllib.parse import urlparse

from pattex.constants.regexes import _URL_TRAILING_NOISE
from pattex.constants.extractor_constants import COMMON_TLDS


def _length_check(text: str, length: int) -> bool:
    """
    Check if the length of the text is less than or equal to the specified length.
    Args:
        text (str): _description_
        length (int): _description_

    Returns:
        bool: True if the length of the text is less than or equal to the specified length, False otherwise.
    """
    return len(text) <= length



def strip_url_noise(url: str) -> str:
    """
    Strip common surrounding noise characters from a raw regex match.

    Removes:
        - Surrounding quotes:   "url"  'url'
        - Angle brackets:       <url>
        - Trailing punctuation: url.  url,  url)  url]  url!  url?  url;  url:
    """
    # strip surrounding angle brackets
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1]

    # strip surrounding quotes (symmetric pairs only)
    if len(url) >= 2 and url[0] == url[-1] and url[0] in ('"', "'"):
        url = url[1:-1]

    # strip trailing noise (may be multi-char, e.g. trailing ").")
    url = _URL_TRAILING_NOISE.sub("", url)

    return url


def is_valid_port(url: str) -> bool:
    """
    Return True if the port number in the URL (if any) is within 1–65535.
    Assumes url has already been stripped of noise.
    """
    try:
        parsed = urlparse(url if "://" in url else "http://" + url)
        if parsed.port is None:
            return True
        return 1 <= parsed.port <= 65535
    except ValueError:
        return False


def extract_tld(host: str) -> str:
    """
    Return the top-level domain label of a hostname.
    e.g. 'www.example.co.uk' → 'uk'
    """
    parts = host.rstrip(".").split(".")
    return parts[-1].lower() if parts else ""


def is_known_tld(host: str) -> bool:
    """
    Return True if the host's TLD is in the curated COMMON_TLDS set.
    Used to gate bare-domain matches in permissive mode.
    """
    return extract_tld(host) in COMMON_TLDS


def normalize_url_host(url: str) -> str:
    """
    Lowercase the scheme and host portions of a URL.
    The path, query, and fragment are left as-is (they are case-sensitive).

    Works for both schemed (https://Example.COM/Path) and
    bare (Example.COM/Path) URLs.
    """
    if "://" in url:
        scheme, rest = url.split("://", 1)
        # isolate host (everything before first / ? or #)
        match = re.match(r"([^/?#]*)(.*)", rest, re.DOTALL)
        if match:
            host_part, tail = match.group(1), match.group(2)
            return scheme.lower() + "://" + host_part.lower() + tail
        return scheme.lower() + "://" + rest
    else:
        match = re.match(r"([^/?#]*)(.*)", url, re.DOTALL)
        if match:
            host_part, tail = match.group(1), match.group(2)
            return host_part.lower() + tail
        return url.lower()


def host_from_url(url: str) -> str:
    """
    Extract just the hostname from a URL (no scheme, port, path, or credentials).
    Works for schemed and bare URLs.
    """
    if "://" in url:
        parsed = urlparse(url)
        return parsed.hostname or ""
    else:
        parsed = urlparse("http://" + url)
        return parsed.hostname or ""