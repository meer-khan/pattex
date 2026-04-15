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

from pattex.constants.regexes import _EMAIL, _URL, _DOMAIN, _IPV4, _IPV6, _SLUG
from pattex._utils._utils import _length_check
# ───────────────────────────── patterns ─────────────────────────────


# ───────────────────────────── extractors ────────────────────────────

# 1. extract all email addresses from the text and return list of dictionary  - DONE
# 2. Do research on RFC 5322 and implement the email extractor according to the standard.
# 3. Introduce a mode parameter to the email extractor that allows users to choose
# between a strict mode (adhering closely to RFC 5322) and a lenient mode (allowing for common
# variations and typos in email addresses).
# Add another funciton whose purpose is only to validate email addresses according to RFC 5322 or normal,
# without extracting them from text.
# Create specific functions (get_valid_gmail_addresses, get_valid_yahoo_addresses, 
# get_valid_outlook_addresses, get_valid_icloud_addresses) that extract and validate email addresses.





def extract_emails(text: str, mode=Literal["practical", "rfc-5322"]) -> list[str]:
    """Extract all email addresses from text."""
    raw_list = _EMAIL.findall(text)

    if mode == "pracical":
        refined_list = []
        # email should not start and end with dot
        # emails's local part should not have special characters other than dot, underscore, hyphen and plus
        # email's domain part should not have special characters other than dot and hyphen
        # email should not have consecutive dots in local part and domain part
        
        for email in raw_list:
            
            local_part, domain_part = email.split("@")
            if len(email) > 320:  # max length of an email address [gmail, yahoo, outlook]
                continue
            if (
                # LOCAL PART RULES
                not local_part.startswith(".")
                and not local_part.endswith(".")
                and ".." not in local_part
                and "--" not in local_part
                and "++" not in local_part
                and all(c.isalnum() or c in "._+-" for c in local_part)
                # DOMAIN PART RULES
                and not domain_part.startswith(".")
                and not domain_part.endswith(".")
                and ".." not in domain_part
                and "--" not in domain_part
                and "++" not in domain_part
                and all(c.isalnum() or c in ".-" for c in domain_part)
                
            ):
                refined_list.append(email)

    return

def validate_gmail_address(email:str)-> bool: 
    pass 

def validate_yahoo_address(email:str)-> bool:
    pass

def validate_outlook_address(email:str)-> bool:
    pass

def validate_icloud_address(email:str)-> bool:
    pass


def extract_emails_legacy(
    text: str, mode=Literal["practical", "rfc-5322"]
) -> list[str]:
    """Extract all email addresses from text."""
    raw_list = _EMAIL.findall(text)

    return raw_list


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
