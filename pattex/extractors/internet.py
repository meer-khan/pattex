"""
It must adhere to technical standards (RFC 5322)

internet.py - Extract internet-related patterns from text.

Extractors:
    - emails
    - urls
    - domains
    - ipv4_addresses
    - ipv6_addresses
    - slugs
"""

from typing import Literal

from pattex.constants.regexes import (
    _EMAIL,
    _URL,
    _DOMAIN,
    _IPV4,
    _IPV6,
    _SLUG,
    _EMAIL_RFC5322,
    _GMAIL_BASE,
    _YAHOO_BASE,
    _OUTLOOK_BASE,
    _ICLOUD_BASE,
    _ZOHO_BASE,
    _PROTON_BASE,
    _CONSECUTIVE_SPECIAL
)
from pattex.constants.extractor_constants import EMAIL_PROVIDERS
from pattex._utils._utils import _length_check
# ───────────────────────────── patterns ─────────────────────────────


# ───────────────────────────── extractors ────────────────────────────

# 1. extract all email addresses from the text and return list of dictionary  - DONE
# 2. Do research on RFC 5322 and implement the email extractor according to the standard.
# 3. Introduce a mode parameter to the email extractor that allows users to choose
# between a strict mode (adhering closely to RFC 5322) and a lenient mode (allowing for common
# variations and typos in email addresses).
# Add another function whose purpose is only to validate email addresses according to RFC 5322 or normal,
# without extracting them from text.
# Create specific functions (get_valid_gmail_addresses, get_valid_yahoo_addresses,
# get_valid_outlook_addresses, get_valid_icloud_addresses) that extract and validate email addresses.

# TODO: Set these rules as constants in some file and use these where needed
def extract_emails(
    text: str, mode: Literal["practical", "rfc5322"] = "practical"
) -> list[str]:
    """
    Extract all email addresses from text.

    Args
    ----------
    text : str
        The input text to extract emails from.
    mode : Literal["practical", "rfc5322"]
        Extraction mode. Default is "practical".

        "practical":
            Covers the vast majority of real-world emails.
            Enforces the following rules:
            - Max total length of 320 characters
            - Local part rules:
                * Only alphanumeric and . _ + - allowed
                * Cannot start or end with a dot
                * No consecutive dots (..)
                * No consecutive hyphens (--)
                * No consecutive plus signs (++)
                * Local part max length 64 characters
            - Domain part rules:
                * Only alphanumeric, dots, and hyphens allowed
                * Cannot start or end with a dot or hyphen
                * No consecutive dots (..)
                * TLD must be at least 2 characters
                * Domain max length 255 characters

        "rfc5322":
            Follows the RFC 5322 specification. More permissive than
            practical mode. Allows:
                * Quoted local parts e.g. "john doe"@example.com
                * Special characters in local part: !#$%&'*+/=?^_`{|}~-
                * IP address literals e.g. user@[192.168.1.1]
                * Escaped characters inside quoted strings
            Does not validate:
                * Comments e.g. (comment)user@example.com
                * Folding whitespace
            Use this mode when parsing emails from raw email headers
            or mail server logs.

    Returns
    -------
    list[str]
        List of extracted email addresses. Empty list if none found.

    Examples
    --------
    >>> extract_emails("contact me at foo@bar.com", mode="practical")
    ['foo@bar.com']

    >>> extract_emails('send to "john doe"@example.com', mode="rfc5322")
    ['"john doe"@example.com']
    """
    raw_list: list[str] = _EMAIL.findall(text)

    if mode == "rfc5322":
        return _EMAIL_RFC5322.findall(text)

    refined_list = []
    if mode == "practical":
        # email should not start and end with dot
        # emails's local part should not have special characters other than dot, underscore, hyphen and plus
        # email's domain part should not have special characters other than dot and hyphen
        # email should not have consecutive dots in local part and domain part

        for email in raw_list:
            local_part, domain_part = email.split("@", maxsplit=1)
            if (
                len(email) > 320
            ):  # max length of an email address [gmail, yahoo, outlook]
                continue

            # local part length check (RFC says max 64)
            if len(local_part) > 64:
                continue

            # domain part length check
            if len(domain_part) > 255:
                continue

            # tld length check
            tld = domain_part.rsplit(".", 1)[-1]
            if len(tld) < 2:
                continue
            if (
                # LOCAL PART RULES
                not local_part.startswith(".")  # no leading dot
                and not local_part.endswith(".")  # no trailing dot
                and not local_part.startswith("-")  # no leading hyphen
                and not local_part.endswith("-")  # no trailing hyphen
                and ".." not in local_part  # no consecutive dots
                and "--" not in local_part  # no consecutive hyphens
                and "++" not in local_part  # no consecutive plus signs
                and all(
                    c.isalnum() or c in "._+-" for c in local_part
                )  # allowed chars only
                # DOMAIN PART RULES
                and not domain_part.startswith(".")  # no leading dot
                and not domain_part.endswith(".")  # no trailing dot
                and not domain_part.startswith("-")  # no leading hyphen
                and not domain_part.endswith("-")  # no trailing hyphen
                and ".." not in domain_part  # no consecutive dots
                and "--" not in domain_part  # no consecutive hyphens
                and "++" not in domain_part  # no consecutive plus
                and all(
                    c.isalnum() or c in ".-" for c in domain_part
                )  # allowed chars only
            ):
                refined_list.append(email)

    return refined_list


def extract_emails_by_provider(text: str, provider: EMAIL_PROVIDERS) -> list[str]:
    """
    Extract emails from text filtered by email provider.

    Args
    ----------
    text : str
        The input text to extract emails from.
    provider : Provider
        The email provider to filter by.
        Supported values: "gmail", "yahoo", "outlook"

    Returns
    -------
    list[str]
        List of extracted emails matching the provider rules.
        Empty list if none found.

    Examples
    --------
    >>> extract_emails_by_provider("contact foo@gmail.com or bar@yahoo.com", "gmail")
    ['foo@gmail.com']

    >>> extract_emails_by_provider("no emails here", "gmail")
    []
    """

    if provider == "gmail":
        return _extract_gmail_emails(text)

    # placeholder for future providers
    # if provider == "yahoo":
    #     return _extract_yahoo_emails(text)
    # if provider == "outlook":
    #     return _extract_outlook_emails(text)

    return []




def validate_gmail_address(email: str) -> bool:
    pass


def validate_yahoo_address(email: str) -> bool:
    pass


def validate_outlook_address(email: str) -> bool:
    pass


def validate_icloud_address(email: str) -> bool:
    pass





def _extract_gmail_emails(text: str) -> list[str]:
    """
    Extract Gmail addresses from text.

    Gmail rules applied:
        Local part:
            - 6 to 30 characters
            - Only letters, numbers, and dots allowed
            - Cannot start or end with a dot
            - No consecutive dots
        Domain:
            - Must be @gmail.com or @googlemail.com
    """

    # first pass — pull anything that looks like a gmail/googlemail address

    raw_list: list[str] = _GMAIL_BASE.findall(text)
    refined_list: list[str] = []

    for email in raw_list:
        local_part, _ = email.split("@", 1)

        # length check
        if len(local_part) < 6:
            continue
        if len(local_part) > 30:
            continue

        # allowed characters — only letters, digits, dots
        if not all(c.isalnum() or c == "." for c in local_part):
            continue

        # no leading dot
        if local_part.startswith("."):
            continue

        # no trailing dot
        if local_part.endswith("."):
            continue

        # no consecutive dots
        if ".." in local_part:
            continue

        refined_list.append(email.lower())  # normalize to lowercase

    return refined_list









def _has_consecutive_specials(local: str) -> bool:
    return bool(_CONSECUTIVE_SPECIAL.search(local))


# ── extractors ───────────────────────────────────────────────────────────────

def _extract_outlook_emails(text: str) -> list[str]:
    """
    Extract Outlook / Hotmail / Live / MSN addresses from text.

    Outlook rules applied:
        Local part:
            - 1 to 64 characters
            - Only letters, numbers, dots, underscores, and hyphens allowed
            - Cannot start or end with a dot or hyphen
            - No consecutive dots (..) or consecutive hyphens (--)
        Domain:
            - Must be @outlook.com, @hotmail.com, @live.com, or @msn.com
    """
    raw_list: list[str] = _OUTLOOK_BASE.findall(text)
    refined_list: list[str] = []

    for email in raw_list:
        local, _ = email.split("@", 1)

        if not (1 <= len(local) <= 64):
            continue

        if not all(c.isalnum() or c in "._-" for c in local):
            continue

        if local[0] in ".-" or local[-1] in ".-":
            continue

        if ".." in local or "--" in local:
            continue

        refined_list.append(email.lower())

    return refined_list


def _extract_icloud_emails(text: str) -> list[str]:
    """
    Extract iCloud / Me / Mac addresses from text.

    iCloud rules applied:
        Local part:
            - 3 to 20 characters
            - Only letters, numbers, dots, underscores, and hyphens allowed
            - Cannot start or end with a dot, underscore, or hyphen
            - No two special characters consecutive (e.g. ._, -., __)
        Domain:
            - Must be @icloud.com, @me.com, or @mac.com
    """
    raw_list: list[str] = _ICLOUD_BASE.findall(text)
    refined_list: list[str] = []

    for email in raw_list:
        local, _ = email.split("@", 1)

        if not (3 <= len(local) <= 20):
            continue

        if not all(c.isalnum() or c in "._-" for c in local):
            continue

        if local[0] in "._-" or local[-1] in "._-":
            continue

        if _has_consecutive_specials(local):
            continue

        refined_list.append(email.lower())

    return refined_list


def _extract_yahoo_emails(text: str) -> list[str]:
    """
    Extract Yahoo addresses from text (global + regional domains).

    Yahoo rules applied:
        Local part:
            - 4 to 32 characters
            - Only letters, numbers, dots, underscores, and hyphens allowed
            - Must start with a letter (a-z)
            - Cannot end with a dot, underscore, or hyphen
            - No two special characters consecutive
        Domain:
            - Must be a recognised Yahoo domain:
              yahoo.com, yahoo.co.uk, yahoo.co.in, yahoo.com.au,
              yahoo.ca, yahoo.de, yahoo.fr, yahoo.es, yahoo.it,
              yahoo.com.br, yahoo.com.mx, yahoo.com.ar
    """
    raw_list: list[str] = _YAHOO_BASE.findall(text)
    refined_list: list[str] = []

    for email in raw_list:
        local, _ = email.split("@", 1)

        if not (4 <= len(local) <= 32):
            continue

        if not all(c.isalnum() or c in "._-" for c in local):
            continue

        if not local[0].isalpha():
            continue

        if local[-1] in "._-":
            continue

        if _has_consecutive_specials(local):
            continue

        refined_list.append(email.lower())

    return refined_list


def _extract_zoho_emails(text: str) -> list[str]:
    """
    Extract Zoho / ZohoMail addresses from text.

    Zoho rules applied:
        Local part:
            - 1 to 60 characters
            - Only letters, numbers, dots, underscores, hyphens, and plus signs allowed
            - Cannot start or end with a dot, underscore, hyphen, or plus
            - No consecutive dots
        Domain:
            - Must be @zoho.com or @zohomail.com
    """
    raw_list: list[str] = _ZOHO_BASE.findall(text)
    refined_list: list[str] = []

    for email in raw_list:
        local, _ = email.split("@", 1)

        if not (1 <= len(local) <= 60):
            continue

        if not all(c.isalnum() or c in "._-+" for c in local):
            continue

        if local[0] in "._-+" or local[-1] in "._-+":
            continue

        if ".." in local:
            continue

        refined_list.append(email.lower())

    return refined_list


def _extract_proton_emails(text: str) -> list[str]:
    """
    Extract Proton / ProtonMail / PM addresses from text.

    Proton rules applied:
        Local part:
            - 1 to 40 characters
            - Only letters, numbers, dots, underscores, and hyphens allowed
            - Cannot start or end with a dot, underscore, or hyphen
            - No consecutive dots
        Domain:
            - Must be @proton.me, @protonmail.com, or @pm.me
    """
    raw_list: list[str] = _PROTON_BASE.findall(text)
    refined_list: list[str] = []

    for email in raw_list:
        local, _ = email.split("@", 1)

        if not (1 <= len(local) <= 40):
            continue

        if not all(c.isalnum() or c in "._-" for c in local):
            continue

        if local[0] in "._-" or local[-1] in "._-":
            continue

        if ".." in local:
            continue

        refined_list.append(email.lower())

    return refined_list







def extract_urls(text: str) -> list[str]:
    """Extract all HTTP/HTTPS URLs from text."""
    return _URL.findall(text)


def extract_domains(text: str) -> list[str]:
    """
    Extract all domain names from text.
    Note: this is intentionally broad — it will also match
    domains inside URLs and emails. Filter downstream if needed.
    """
    return _DOMAIN.findall(text)


def extract_ipv4_addresses(text: str) -> list[str]:
    """Extract all valid IPv4 addresses from text."""
    return _IPV4.findall(text)


def extract_ipv6_addresses(text: str) -> list[str]:
    """Extract all IPv6 addresses from text."""
    return _IPV6.findall(text)


def extract_slugs(text: str) -> list[str]:
    """Extract URL slugs (e.g. 'my-blog-post') from text."""
    return _SLUG.findall(text)
