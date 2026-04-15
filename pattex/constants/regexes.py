import re

# ------------------ Email ----------------------
_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE,
)

_EMAIL_RFC5322 = re.compile(
    r"""(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"""   # unquoted local part
    r"""(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*""" # dots in local part
    r"""|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]"""  # quoted string
    r"""|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")"""    # escaped chars in quotes
    r"""@"""
    r"""(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"""  # domain label
    r"""(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)"""  # more labels
    r"""|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"""  # ip literal
    r"""(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\])""",          # last octet
    re.VERBOSE,
)
_EMAIL_RFC5322 = re.compile(
    # ================================================================
    # LOCAL PART (before the @)
    # The local part can be either:
    #   A) Unquoted   — plain characters with optional dots
    #   B) Quoted     — wrapped in double quotes, allows spaces etc.
    # ================================================================

    # ── A) UNQUOTED LOCAL PART ───────────────────────────────────────
    # Matches one or more allowed characters (no spaces, no quotes)
    # Allowed: letters, digits, and special chars !#$%&'*+/=?^_`{|}~-
    #
    # Examples that match:
    #   john.doe        → plain name with dot
    #   user+filter     → plus addressing (gmail style)
    #   user_name       → underscore
    #   john!doe        → exclamation mark
    #   x               → single character
    #
    # Examples that do NOT match:
    #   john doe        → space not allowed in unquoted
    #   john@doe        → @ not allowed
    #   (comment)john   → parentheses not allowed in unquoted
    r"""(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"""

    # ── DOTS IN UNQUOTED LOCAL PART ──────────────────────────────────
    # Allows dots BETWEEN characters but not at start, end,
    # or consecutively (..would be two groups with nothing between)
    #
    # Examples that match:
    #   john.doe        → one dot
    #   john.m.doe      → multiple dots
    #
    # Examples that do NOT match:
    #   .john           → leading dot (nothing before the dot group)
    #   john.           → trailing dot (nothing after)
    #   john..doe       → consecutive dots (empty segment between)
    r"""(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"""

    # ── B) QUOTED LOCAL PART ─────────────────────────────────────────
    # Wraps the local part in double quotes.
    # Allows characters that are normally forbidden in unquoted form.
    #
    # Examples that match:
    #   "john doe"      → space inside quotes
    #   "john@doe"      → @ inside quotes
    #   "very.unusual.@.unusual.com"  → dots and @ inside quotes
    #   " "             → just a space
    #   "john..doe"     → consecutive dots allowed inside quotes
    #
    # Examples that do NOT match:
    #   "john           → unclosed quote
    #   john"           → quote not at start
    r"""|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]"""
    # ↑ allowed raw characters inside quotes (ASCII printable minus
    #   \x22 which is " and \x5c which is \)
    # \x01-\x08  → control chars (SOH to BS)
    # \x0b       → vertical tab
    # \x0c       → form feed
    # \x0e-\x1f  → more control chars (SO to US)
    # \x21       → ! (skipping \x20 which is space... wait, space IS
    #              allowed inside quotes, this is a known simplification)
    # \x23-\x5b  → # through [ (skipping \x22 which is ")
    # \x5d-\x7f  → ] through DEL (skipping \x5c which is \)

    # ── ESCAPED CHARACTERS INSIDE QUOTES ─────────────────────────────
    # Inside a quoted string, any character can be escaped with \
    # This is how you include a literal " or \ inside a quoted local part
    #
    # Examples that match (inside quotes):
    #   \"          → escaped double quote → allows: "john\"doe"@x.com
    #   \\          → escaped backslash   → allows: "john\\doe"@x.com
    #   \n          → escaped newline (rare but RFC allows it)
    #
    # \x01-\x09  → SOH to HT
    # \x0b       → vertical tab
    # \x0c       → form feed
    # \x0e-\x7f  → SO to DEL
    r"""|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")"""

    # ── THE @ SEPARATOR ──────────────────────────────────────────────
    r"""@"""

    # ================================================================
    # DOMAIN PART (after the @)
    # The domain can be either:
    #   A) Named domain  — standard hostname like gmail.com
    #   B) IP literal    — address in brackets like [192.168.1.1]
    # ================================================================

    # ── A) NAMED DOMAIN ──────────────────────────────────────────────
    # A domain label is a segment between dots.
    # Each label: starts and ends with alphanumeric,
    #             middle can have hyphens,
    #             max 63 characters per label (0,61 middle + 2 ends)
    #
    # Examples that match:
    #   gmail.com           → two labels
    #   mail.company.co.uk  → four labels
    #   x.io                → short TLD
    #   my-company.com      → hyphen in label
    #   xn--nxasmq6b.com    → internationalized domain (punycode)
    #
    # Examples that do NOT match:
    #   -gmail.com          → label starts with hyphen
    #   gmail-.com          → label ends with hyphen
    #   gmail..com          → empty label (consecutive dots)
    #   a_b.com             → underscore not allowed in domain
    r"""(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"""
    r"""(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)"""

    # ── B) IP ADDRESS LITERAL ─────────────────────────────────────────
    # Domain can be an IPv4 address wrapped in square brackets.
    # Each octet validated: 0-255
    #   25[0-5]       → 250-255
    #   2[0-4][0-9]   → 200-249
    #   [01]?[0-9][0-9]? → 0-199
    #
    # Examples that match:
    #   [192.168.1.1]   → private network
    #   [127.0.0.1]     → localhost
    #   [255.255.255.0] → broadcast
    #   [0.0.0.0]       → any address
    #
    # Examples that do NOT match:
    #   [256.1.1.1]     → 256 out of range
    #   [192.168.1]     → only 3 octets
    #   192.168.1.1     → no brackets
    #   [192.168.1.1    → unclosed bracket
    r"""|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"""
    r"""(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\])""",

    re.VERBOSE,
)


_GMAIL_BASE = re.compile(
        r"[a-zA-Z0-9.]+@(?:gmail|googlemail)\.com",
        re.IGNORECASE,
    )
# --------------------------------------------------
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