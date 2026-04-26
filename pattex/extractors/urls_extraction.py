from typing import Literal
import re
from pattex.constants.regexes import (
    _URL_BARE_DOMAIN,
    _URL_BARE_IP,
    _URL_LOCALHOST,
    _URL_PROTOCOL_RELATIVE,
    _URL_STRICT_BASE,
    
)
from pattex._utils._utils import  host_from_url, normalize_url_host, is_valid_port, strip_url_noise, is_known_tld

# ─────────────────────────────────────────────────────────────────────────────
# URL EXTRACTORS
# ─────────────────────────────────────────────────────────────────────────────
 
 
def extract_urls(
    text: str,
    mode: Literal["strict", "permissive"] = "strict",
    include_localhost: bool = False,
) -> list[str]:
    """
    Extract URLs from text.
 
    Args:
        text:              Input string to search.
        mode:              Extraction strictness.
 
            - ``"strict"`` *(default)* — only schemed URLs
              (``http``, ``https``, ``ftp``, ``ftps``, ``sftp``,
              ``ws``, ``wss``). Port must be 1–65535 if present.
              Highest precision, lowest false-positive rate.
 
            - ``"permissive"`` — additionally matches:
                - Protocol-relative URLs starting with ``//``
                - Bare domain URLs (no scheme) whose TLD is in the
                  curated ``COMMON_TLDS`` list
                - Bare IPv4 addresses with an optional path/query
                - ``localhost`` with an optional port and path
 
        include_localhost: When ``True``, ``localhost`` URLs are included
                           even in ``"strict"`` mode. Defaults to ``False``.
 
    Returns:
        Deduplicated list of URL strings, with scheme and host lowercased.
        Trailing punctuation and surrounding quotes are stripped.
        Order preserves first-occurrence order from left to right in text.
 
    Rules applied to all modes:
        - Trailing noise stripped: ``. , ! ? ; : ' " ) > ]``
        - Surrounding quotes stripped
        - Port number validated: must be in range 1–65535
        - Duplicate URLs removed (case-insensitive on scheme+host)
        - Scheme and host normalised to lowercase
 
    Additional rules for strict mode:
        - Scheme must be one of: http, https, ftp, ftps, sftp, ws, wss
 
    Additional rules for permissive mode (on top of strict):
        - Protocol-relative (``//host``) URLs accepted
        - Bare domain URLs accepted if TLD is in COMMON_TLDS
        - Bare IPv4 URLs accepted
        - ``localhost`` accepted (with or without port)
    """
    seen: set[str] = set()
    results: list[str] = []
 
    def _add(url: str) -> None:
        url = strip_url_noise(url)
        if not url:
            return
        if not is_valid_port(url):
            return
        normalised = normalize_url_host(url)
        key = normalised.lower()
        if key not in seen:
            seen.add(key)
            results.append(normalised)
 
    # ── strict: schemed URLs ──────────────────────────────────────────────────
    for match in _URL_STRICT_BASE.finditer(text):
        _add(match.group(0))
 
    # ── localhost (opt-in for strict; always on for permissive) ───────────────
    if include_localhost or mode == "permissive":
        for match in _URL_LOCALHOST.finditer(text):
            raw = match.group(0)
            # avoid double-counting localhost already caught by strict base
            if not raw.startswith(("http://", "https://")):
                _add(raw)
 
    if mode == "permissive":
        # ── protocol-relative //host ──────────────────────────────────────────
        for match in _URL_PROTOCOL_RELATIVE.finditer(text):
            raw = match.group(0)
            _add(raw)
 
        # ── bare domain URLs ──────────────────────────────────────────────────
        for match in _URL_BARE_DOMAIN.finditer(text):
            raw = match.group(0)
            raw_clean = strip_url_noise(raw)
            host = host_from_url(raw_clean)
            if not is_known_tld(host):
                continue
            # skip if it's an email address fragment
            start = match.start()
            if start > 0 and text[start - 1] == "@":
                continue
            _add(raw)
 
        # ── bare IPv4 ─────────────────────────────────────────────────────────
        for match in _URL_BARE_IP.finditer(text):
            raw = match.group(0)
            # skip IPs that are already part of a schemed URL already captured
            start = match.start()
            if start >= 3 and text[start - 3: start] == "://":
                continue
            _add(raw)
 
    return results
 
 
def extract_urls_by_scheme(
    text: str,
    scheme: Literal["http", "https", "ftp", "ftps", "sftp", "ws", "wss"],
) -> list[str]:
    """
    Extract URLs that use a specific scheme.
 
    Args:
        text:   Input string to search.
        scheme: One of ``"http"``, ``"https"``, ``"ftp"``, ``"ftps"``,
                ``"sftp"``, ``"ws"``, ``"wss"``.
 
    Returns:
        Deduplicated list of URL strings using the given scheme,
        with host lowercased and trailing noise stripped.
 
    Rules applied:
        - Scheme must match exactly (case-insensitive)
        - Port number must be in range 1–65535 if present
        - Trailing noise stripped: ``. , ! ? ; : ' " ) > ]``
        - Duplicate URLs removed
    """
    pattern = re.compile(
        re.escape(scheme) + r"://" +
        r"(?:[a-zA-Z0-9._~!$&'()*+,;=%-]+(?::[a-zA-Z0-9._~!$&'()*+,;=:%-]*)?@)?" +
        r"(?:"
        r"\[(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\]"  # IPv6
        r"|(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"  # IPv4
        r"|(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}"  # domain
        r"|localhost"
        r")"
        r"(?::\d{1,5})?"
        r"(?:/[^\s\"'<>()\[\]{}|\\^`]*)?"
        r"(?:\?[^\s\"'<>()\[\]{}|\\^`#]*)?"
        r"(?:#[^\s\"'<>()\[\]{}|\\^`]*)?",
        re.IGNORECASE,
    )
 
    seen: set[str] = set()
    results: list[str] = []
 
    for match in pattern.finditer(text):
        url = strip_url_noise(match.group(0))
        if not url:
            continue
        if not is_valid_port(url):
            continue
        normalised = normalize_url_host(url)
        key = normalised.lower()
        if key not in seen:
            seen.add(key)
            results.append(normalised)
 
    return results
 
 
def extract_urls_by_domain(
    text: str,
    domain: str,
    mode: Literal["strict", "permissive"] = "strict",
) -> list[str]:
    """
    Extract all URLs belonging to a specific domain (and its subdomains).
 
    Args:
        text:   Input string to search.
        domain: Base domain to filter on, e.g. ``"example.com"``.
                Subdomains are included automatically
                (``api.example.com``, ``www.example.com``).
        mode:   Passed through to :func:`extract_urls`.
 
    Returns:
        Subset of URLs from :func:`extract_urls` whose host equals
        ``domain`` or ends with ``".{domain}"``.
 
    Example::
 
        extract_urls_by_domain(text, "github.com")
        # returns https://github.com/..., https://api.github.com/..., etc.
    """
    all_urls = extract_urls(text, mode=mode)
    domain_lower = domain.lower().lstrip(".")
 
    filtered: list[str] = []
    for url in all_urls:
        host = host_from_url(url).lower()
        if host == domain_lower or host.endswith("." + domain_lower):
            filtered.append(url)
 
    return filtered




