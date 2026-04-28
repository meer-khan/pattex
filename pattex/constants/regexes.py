import re

# ------------------ Email ----------------------
_EMAIL = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE,
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

# * Allowed characters in local part (part before @): 
# small alphabets a-z
# digits 0-9
# capital alphabets A-Z
# dots

#* Not allowed characters in local part (part before @):
# spaces
# parentheses
# backslash
# consecutive dots
# start with dot 
# end with dot
# special characters !#$%^&*()+=,;:'"?><[]{}|~`
_GMAIL_BASE = re.compile(
        r"[a-zA-Z0-9.]+@(?:gmail|googlemail)\.com",
        re.IGNORECASE,
    )


# Outlook / Hotmail / Live personal account email rules
#
# Supported domains commonly include:
# @outlook.com
# @hotmail.com
# @live.com
# @msn.com
#
# =========================================================
# Allowed characters in local part (part before @)
# =========================================================
#
# small alphabets a-z
# capital alphabets A-Z
# digits 0-9
# dots (.)
# underscores (_)
# hyphens (-)
#
# In many practical cases, plus (+) addressing is also supported
# for receiving mail (example: john+work@outlook.com)
#
#
# =========================================================
# Not allowed characters in local part (part before @)
# =========================================================
#
# spaces
# parentheses ()<>[]{},;:'"\/|`~!#$%^&*=?

# =========================================================
# Structural restrictions in local part
# =========================================================
#
# cannot start with dot (.)
# cannot end with dot (.)
# cannot have consecutive dots (..)
_OUTLOOK_BASE = re.compile(
    r"[a-zA-Z0-9._-]+@(?:outlook|hotmail|live|msn)\.com",
    re.IGNORECASE,
)


# Supported domains commonly include:
# @icloud.com
# @me.com
# @mac.com
#
# Note:
# @me.com and @mac.com are older Apple domains.
# Existing users may still use them.
#
# =========================================================
# Allowed characters in local part (part before @)
# =========================================================
#
# small alphabets a-z
# capital alphabets A-Z
# digits 0-9
# dots (.)
# underscores (_)
# hyphens (-)
# plus (+) addressing is commonly supported for receiving mail
# example:
# john+work@icloud.com
#
#
# =========================================================
# Not allowed characters in local part (part before @)
# =========================================================
#
# spaces , ()<>[]{},;:'"\/|`~!#$%^&*=?

# =========================================================
# Structural restrictions in local part
# =========================================================
#
# cannot start with dot (.)
# cannot end with dot (.)
# cannot have consecutive dots (..)
_ICLOUD_BASE = re.compile(
    r"[a-zA-Z0-9._-]+@(?:icloud|me|mac)\.com",
    re.IGNORECASE,
)


# =========================================================
# Supported domains commonly include:
# @yahoo.com
# @yahoo.co.uk
# @yahoo.ca
# @yahoo.in
# @ymail.com
# @rocketmail.com
#
# Note:
# @rocketmail.com is an older Yahoo domain.
# Existing users may still use it.
#
# =========================================================
# Allowed characters in local part (part before @)
# =========================================================
#
# small alphabets a-z
# capital alphabets A-Z
# digits 0-9
# dots (.)
# underscores (_)
#
# hyphens (-) may be allowed depending on account type
# and legacy account behavior, but are not always reliable
#
# plus (+) addressing may work for aliases/filters,
# but should not be assumed for base account creation
#
#
# =========================================================
# Not allowed characters in local part (part before @)
# =========================================================
#
# spaces ()<>[]{},;:'"\/|`~!#$%^&*=?
# =========================================================
# Structural restrictions in local part
# =========================================================
#
# cannot start with dot (.)
# cannot end with dot (.)
# cannot have consecutive dots (..)
_YAHOO_BASE = re.compile(
    r"[a-zA-Z0-9._-]+"
    r"@yahoo\.(?:com|co\.uk|co\.in|com\.au|ca|de|fr|es|it|com\.br|com\.mx|com\.ar)",
    re.IGNORECASE,
)


# =========================================================
# Supported domains commonly include:
# @zohomail.com
# custom domains via Zoho Mail hosting
#
# Note:
# Zoho is commonly used for both personal and business
# email accounts, especially with custom domains.
#
# =========================================================
# Allowed characters in local part (part before @)
# =========================================================
#
# small alphabets a-z
# capital alphabets A-Z
# digits 0-9
# dots (.)
# underscores (_)
# hyphens (-)
#
# plus (+) addressing is commonly supported
# example:
# john+work@zohomail.com
#
#
# =========================================================
# Not allowed characters in local part (part before @)
# =========================================================
#
# spaces ()<>[]{},;:'"\/|`~!#$%^&*=?

# =========================================================
# Structural restrictions in local part
# =========================================================
#
# cannot start with dot (.)
# cannot end with dot (.)
# cannot have consecutive dots (..)
_ZOHO_BASE = re.compile(
    r"[a-zA-Z0-9._+\-]+@(?:zoho|zohomail)\.com",
    re.IGNORECASE,
)



# =========================================================
# Proton Mail personal account email rules
# =========================================================
#
# Supported domains commonly include:
# @proton.me
# @protonmail.com
# @pm.me
#
# Note:
# @pm.me is a short alias domain provided by Proton
#
#
# =========================================================
# Allowed characters in local part (part before @)
# =========================================================
#
# small alphabets a-z
# capital alphabets A-Z
# digits 0-9
# dots (.)
# underscores (_)
# hyphens (-)
#
# plus (+) addressing is commonly supported
# example:
# john+work@proton.me
#
#
# =========================================================
# Not allowed characters in local part (part before @)
# =========================================================
#
# spaces ()<>[]{},;:'"\/|`~!#$%^&*=?

# =========================================================
# Structural restrictions in local part
# =========================================================
#
# cannot start with dot (.)
# cannot end with dot (.)
# cannot have consecutive dots (..)
_PROTON_BASE = re.compile(
    r"[a-zA-Z0-9._-]+@(?:proton\.me|protonmail\.com|pm\.me)",
    re.IGNORECASE,
)


 
# ── URL shared sub-patterns ───────────────────────────────────────────────────
 
_USERINFO = (
    r"(?:[a-zA-Z0-9._~!$&'()*+,;=%-]+"
    r"(?::[a-zA-Z0-9._~!$&'()*+,;=:%-]*)?)@"
)
_IPV4 = (
    r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
)
_IPV6    = r"\[(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\]"
_DOMAIN  = r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}"
_PORT    = r"(?::\d{1,5})?"
 
# Tail: optional path, then optional query+fragment captured together.
_TAIL = (
    r"(?:"
    r"/[^\s\"'<>()\[\]{}|\\^]*"
    r"(?:[?#][^\s\"'<>()\[\]{}|\\^]*)?"
    r")?"
)
 
# ── Schemed URL (strict mode) ─────────────────────────────────────────────────
 
_URL_STRICT_BASE = re.compile(
    r"(?:https?|ftps?|sftp|wss?)"
    r"://"
    r"(?:" + _USERINFO + r")?"
    r"(?:" + _IPV6 + r"|" + _IPV4 + r"|" + _DOMAIN + r"|localhost)"
    + _PORT + _TAIL,
    re.IGNORECASE,
)
 
# ── Protocol-relative  //host/path ───────────────────────────────────────────
 
_URL_PROTOCOL_RELATIVE = re.compile(
    r"//"
    r"(?:" + _DOMAIN + r"|" + _IPV4 + r"|localhost)"
    + _PORT + _TAIL,
    re.IGNORECASE,
)
 
# ── Bare domain (permissive) ──────────────────────────────────────────────────
 
_URL_BARE_DOMAIN = re.compile(
    r"(?<![/@:\w.])"
    r"(?:www\.)?"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}"
    + _PORT + _TAIL,
    re.IGNORECASE,
)
 
# ── Bare IPv4 (permissive) ────────────────────────────────────────────────────
 
_URL_BARE_IP = re.compile(
    r"(?<![/@:\w.])"
    + _IPV4
    + _PORT + _TAIL,
    re.IGNORECASE,
)
 
# ── Localhost ─────────────────────────────────────────────────────────────────
 
_URL_LOCALHOST = re.compile(
    r"(?<!\w)localhost" + _PORT + _TAIL,
    re.IGNORECASE,
)
 
# ── Trailing noise ────────────────────────────────────────────────────────────
 
_URL_TRAILING_NOISE = re.compile(r"[.,!?;:'\")>\]]+$")
 

















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




# ── base regexes ────────────────────────────────────────────────────────────


# ── helpers ──────────────────────────────────────────────────────────────────

_CONSECUTIVE_SPECIAL = re.compile(r"[._-]{2,}")