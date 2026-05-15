from functools import lru_cache
from typing import Literal
import re

from pattex.constants.regexes import (
    # _URL_BARE_DOMAIN,
    # _URL_BARE_IP,
    _URL_LOCALHOST,
    # _URL_PROTOCOL_RELATIVE,
    _SCHEMES,
    _IPV4,
    _IPV6,
    _DOMAIN,
    _PORT,
    _USERINFO,
    _TAIL,
    _BARE_DOMAIN,
)
from pattex._utils._utils import (
    host_from_url,
    normalize_url_host,
    is_valid_port,
    strip_url_noise,
    is_known_tld,
)
from pattex.constants.extractor_constants import URL_MODES, URL_SCHEMES
# ─────────────────────────────────────────────────────────────────────────────
# URL EXTRACTORS
# ─────────────────────────────────────────────────────────────────────────────


@lru_cache(maxsize=16)
def _build_strict_regex(
    allow_ipv4: bool,
    allow_ipv6: bool,
    allow_port: bool,
    allow_tail: bool,
    schemes: list[str] | None,
) -> re.Pattern:
    scheme_pattern = "|".join(schemes) if schemes else _SCHEMES

    host_parts = []
    if allow_ipv6:
        host_parts.append(_IPV6)
    if allow_ipv4:
        host_parts.append(_IPV4)
    host_parts.append(_DOMAIN)
    host_parts.append("localhost")

    host = "|".join(host_parts)
    port = _PORT if allow_port else r""
    tail = _TAIL if allow_tail else r""

    pattern = (
        r"(?:" + scheme_pattern + r")"
        r"://"
        r"(?:" + _USERINFO + r")?"
        r"(?:" + host + r")" + port + tail
    )
    return re.compile(pattern, re.IGNORECASE)

@lru_cache(maxsize=2)  # only two modes
def _build_permissive_regex(
    allow_localhost: bool,
) -> re.Pattern:
    parts = [
        r"(?P<protocol_relative>//" + r"(?:" + _DOMAIN + r"|" + _IPV4 + r"|localhost)" + _PORT + _TAIL + r")",
       r"(?P<bare_domain>" + _BARE_DOMAIN + _PORT + _TAIL + r")",
        r"(?P<bare_ip>(?<![/@:\w.])" + _IPV4 + _PORT + _TAIL + r")",
    ]
    if allow_localhost:
        parts.append(r"(?P<localhost>(?<!\w)localhost" + _PORT + _TAIL + r")")

    return re.compile("|".join(parts), re.IGNORECASE)

def extract_urls(
    text: str,
    mode: URL_MODES = "strict",
    allow_localhost: bool = False,
    allow_ipv4: bool = True,
    allow_ipv6: bool = True,
    allow_port: bool = True,
    allow_tail: bool = True,
    schemes: list[str] | None = None,
) -> list[str]:
    """
    Extract URLs from text.

    Args:
        text:              Input string to search.
        mode:              Extraction strictness.

            - ``"strict"`` *(default)* — only schemed URLs.
              Highest precision, lowest false-positive rate.

            - ``"permissive"`` — additionally matches protocol-relative,
              bare domains, bare IPv4, and localhost URLs.

        include_localhost: Include localhost URLs in strict mode. Default False.
        allow_ipv4:        Match IPv4 addresses. Default True.
        allow_ipv6:        Match IPv6 addresses. Default True.
        allow_port:        Match URLs with port numbers. Default True.
        allow_tail:        Match URL path, query, and fragment. Default True.
        schemes:           Restrict to specific schemes e.g. ``("https", "ftp")``.
                           Defaults to all supported schemes.

    Returns:
        Deduplicated list of URL strings, scheme and host lowercased.
        Order preserves first-occurrence from left to right.
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

    def _is_inside_schemed_url(match_start: int) -> bool:
        preceding = text[max(0, match_start - 10): match_start]
        return "://" in preceding or preceding.endswith(":")

    # ── strict: always runs ───────────────────────────────────────────────────
    strict_re = _build_strict_regex(allow_ipv4, allow_ipv6, allow_port, allow_tail, schemes)
    for match in strict_re.finditer(text):
        _add(match.group(0))

    # ── localhost in strict mode ──────────────────────────────────────────────
    if allow_localhost and mode == "strict":
        for match in _URL_LOCALHOST.finditer(text):
            if not _is_inside_schemed_url(match.start()):
                _add(match.group(0))

    # ── permissive: single scan via combined regex ────────────────────────────
    if mode == "permissive":
        permissive_re = _build_permissive_regex(allow_localhost = True)
        for match in permissive_re.finditer(text):
            if match.lastgroup in ("protocol_relative", "bare_ip", "localhost"):
                if not _is_inside_schemed_url(match.start()):
                    _add(match.group(0))
            elif match.lastgroup == "bare_domain":
                if match.start() > 0 and text[match.start() - 1] == "@":
                    continue
                host = host_from_url(strip_url_noise(match.group(0)))
                if is_known_tld(host):
                    _add(match.group(0))

    return results

def extract_urls_by_scheme(
    text: str,
    scheme: URL_SCHEMES,
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
    return extract_urls(text, schemes=(scheme,))

def extract_urls_by_domain(
    text: str,
    domain: str,
    include_subdomains: bool = True,
    mode: URL_MODES = "strict",
) -> list[str]:
    """
    Extract URLs that belong to a specific domain.

    Args:
        text:               Input string to search.
        domain:             Domain to filter by e.g. ``"google.com"``.
        include_subdomains: When ``True`` (default), matches subdomains too
                            e.g. ``"sub.google.com"`` matches ``"google.com"``.
                            When ``False``, only exact domain matches are returned.
        mode:               Extraction strictness. Defaults to ``"strict"``.

    Returns:
        Deduplicated list of URL strings belonging to the given domain,
        with host lowercased and trailing noise stripped.
    """
    domain = domain.lower().strip()
    all_urls = extract_urls(text, mode=mode)

    result = []
    for url in all_urls:
        host = host_from_url(url).lower()
        if include_subdomains:
            if host == domain or host.endswith("." + domain):
                result.append(url)
        else:
            if host == domain:
                result.append(url)

    return result

# TODO: Extract only Local hosts 
# Extract only IPV4 and IPV6 (both in same function OPTIONAL)




def extract_localhost_urls(
    text: str,
    allow_port: bool = True,
    allow_tail: bool = True,
) -> list[str]:
    """
    Extract URLs whose host is localhost.

    Args:
        text:         Input string to search.
        allow_port:   Include URLs with a port number. Default True.
        allow_tail:   Include URLs with a path, query, or fragment. Default True.

    Returns:
        Deduplicated list of localhost URL strings,
        with scheme lowercased and trailing noise stripped.
    """
    return extract_urls(
        text,
        mode="strict",
        allow_localhost=True,
        allow_ipv4=False,
        allow_ipv6=False,
        allow_port=allow_port,
        allow_tail=allow_tail,
    )




# ------------------------------- VALIDATION HELPERS ---------------------------
def is_url(text: str) -> bool:
    """
    Check if the given string is a valid URL.

    Args:
        text: Input string to check.

    Returns:
        True if the string is a valid URL, False otherwise.

    Rules applied:
        - Scheme must be one of: http, https, ftp, ftps, sftp, ws, wss
        - Port number must be in range 1–65535 if present
        - Host must be a valid domain, IPv4, IPv6, or localhost
    """
    urls = extract_urls(text.strip(), mode="strict")
    return len(urls) == 1 and urls[0].rstrip("/") == text.strip().rstrip("/")


def _get_root_domain(host: str) -> str:
    """
    Extract root domain from a hostname.
    e.g. "api.google.com" → "google.com"
         "google.com"     → "google.com"
    """
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) > 2 else host


def extract_unique_domains(
    text: str,
    root_only: bool = False,
    mode: URL_MODES = "strict",
) -> list[str]:
    """
    Extract unique domains from all URLs found in text.

    Args:
        text:      Input string to search.
        root_only: When ``True``, returns root domains only e.g.
                   ``"api.google.com"`` → ``"google.com"``.
                   When ``False`` (default), returns full hostnames.
        mode:      Extraction strictness. Defaults to ``"strict"``.

    Returns:
        Deduplicated list of domain strings, lowercased,
        in first-occurrence order.
    """
    all_urls = extract_urls(text, mode=mode)

    seen: set[str] = set()
    results: list[str] = []

    for url in all_urls:
        host = host_from_url(url)
        if not host:
            continue
        domain = _get_root_domain(host) if root_only else host
        if domain not in seen:
            seen.add(domain)
            results.append(domain)

    return results



def extract_urls_by_tld(
    text: str,
    tld: str,
    mode: URL_MODES = "strict",
) -> list[str]:
    """
    Extract URLs whose domain ends with a specific TLD.

    Args:
        text:  Input string to search.
        tld:   TLD to filter by e.g. ``"com"``, ``"io"``, ``"co.uk"``.
               Leading dot is optional — both ``"com"`` and ``".com"`` work.
        mode:  Extraction strictness. Defaults to ``"strict"``.

    Returns:
        Deduplicated list of URL strings whose host ends with the given TLD,
        with scheme and host lowercased and trailing noise stripped.
    """
    tld = tld.lower().lstrip(".")  # normalize — strip leading dot if present

    all_urls = extract_urls(text, mode=mode)

    return [
        url for url in all_urls
        if host_from_url(url).endswith("." + tld)
    ]


def extract_secure_urls(text: str) -> list[str]:
    """
    Extract URLs that use a secure scheme (https, ftps, sftp, wss).

    Args:
        text:  Input string to search.

    Returns:
        Deduplicated list of secure URL strings,
        with scheme and host lowercased and trailing noise stripped.
    """
    return extract_urls(text, schemes=("https", "ftps", "sftp", "wss"))


def extract_insecure_urls(text: str) -> list[str]:
    """
    Extract URLs that use an insecure scheme (http, ftp, ws).

    Args:
        text:  Input string to search.

    Returns:
        Deduplicated list of insecure URL strings,
        with scheme and host lowercased and trailing noise stripped.
    """
    return extract_urls(text, schemes=("http", "ftp", "ws"))


def extract_urls_with_auth(text: str) -> list[str]:
    """
    Extract URLs that contain authentication credentials (user:pass@host).

    Args:
        text:  Input string to search.

    Returns:
        Deduplicated list of URL strings containing userinfo,
        with scheme and host lowercased and trailing noise stripped.
    """
    from urllib.parse import urlparse

    all_urls = extract_urls(text)

    return [
        url for url in all_urls
        if urlparse(url).username is not None
    ]


def extract_urls_with_port(
    text: str,
    port: int | None = None,
) -> list[str]:
    """
    Extract URLs that contain a port number.

    Args:
        text:  Input string to search.
        port:  Specific port to filter by e.g. ``8080``.
               When ``None`` (default), returns all URLs that have any port.

    Returns:
        Deduplicated list of URL strings containing a port,
        with scheme and host lowercased and trailing noise stripped.
    """
    from urllib.parse import urlparse

    all_urls = extract_urls(text)

    return [
        url for url in all_urls
        if (p := urlparse(url).port) is not None
        and (port is None or p == port)
    ]
