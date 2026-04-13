import re

_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE,
)

_URL = re.compile(
    r"https?://"                        # scheme
    r"(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}"  # host
    r"(?::\d{1,5})?"                    # optional port
    r"(?:/[^\s]*)?",                    # optional path/query
    re.IGNORECASE,
)

_DOMAIN = re.compile(
    r"\b(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}\b",
    re.IGNORECASE,
)

_IPV4 = re.compile(
    r"\b"
    r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    r"\b"
)

_IPV6 = re.compile(
    r"\b"
    r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}"        # full
    r"|(?:[0-9a-fA-F]{1,4}:){1,7}:"                      # trailing ::
    r"|:(?::[0-9a-fA-F]{1,4}){1,7}"                      # leading ::
    r"|::(?:ffff(?::0{1,4})?:)?"                          # ::ffff:
    r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
    r"\b",
    re.IGNORECASE,
)

_SLUG = re.compile(
    r"\b[a-z0-9]+(?:-[a-z0-9]+)+\b"
)