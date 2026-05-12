from pattex.constants.regexes import _OUTLOOK_BASE, _ICLOUD_BASE, _ZOHO_BASE, _PROTON_BASE, _GMAIL_BASE, _YAHOO_BASE, _URL_STRICT_BASE

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
#
# examples:
# .john@outlook.com        -> invalid
# john.@outlook.com        -> invalid
# john..smith@outlook.com  -> invalid
#
#
# =========================================================
# Domain rules
# =========================================================
#
# domain must be valid and resolvable
# no spaces allowed
# no consecutive dots
# domain labels cannot start with hyphen (-)
# domain labels cannot end with hyphen (-)
#
# examples:
# john@-example.com        -> invalid
# john@example-.com        -> invalid
# john@example..com        -> invalid
#
#
# =========================================================
# Practical Outlook behavior
# =========================================================
#
# unlike Gmail, dots are NOT ignored
#
# johnsmith@outlook.com
# john.smith@outlook.com
#
# these may be treated as different accounts
#
#
# =========================================================
# Important note
# =========================================================
#
# Microsoft does not publicly expose strict full validation
# rules like RFC specs, so production systems usually use
# practical validation rules rather than strict RFC compliance.
#
# For library design, prefer:
# practical validation > theoretical RFC completeness
#
_OUTLOOK_BASE




# =========================================================
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
#
# examples:
# .john@icloud.com         -> invalid
# john.@icloud.com         -> invalid
# john..smith@icloud.com   -> invalid
#
#
# =========================================================
# Domain rules
# =========================================================
#
# domain must be valid and resolvable
# no spaces allowed
# no consecutive dots
# domain labels cannot start with hyphen (-)
# domain labels cannot end with hyphen (-)
#
# examples:
# john@-example.com        -> invalid
# john@example-.com        -> invalid
# john@example..com        -> invalid
#
#
# =========================================================
# Practical iCloud behavior
# =========================================================
#
# dots are treated as real characters
# unlike Gmail, dots are NOT ignored
#
# johnsmith@icloud.com
# john.smith@icloud.com
#
# these may be treated as different accounts
#
#
# =========================================================
# Important note
# =========================================================
#
# Apple does not publicly expose full strict validation
# specifications for iCloud addresses.
#
# Production systems usually rely on practical validation
# rather than strict RFC compliance.
#
# For library design, prefer:
# practical validation > theoretical RFC completeness
#
_ICLOUD_BASE




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
#
# examples:
# .john@yahoo.com         -> invalid
# john.@yahoo.com         -> invalid
# john..smith@yahoo.com   -> invalid
#
#
# =========================================================
# Domain rules
# =========================================================
#
# domain must be valid and resolvable
# no spaces allowed
# no consecutive dots
# domain labels cannot start with hyphen (-)
# domain labels cannot end with hyphen (-)
#
# examples:
# john@-example.com       -> invalid
# john@example-.com       -> invalid
# john@example..com       -> invalid
#
#
# =========================================================
# Practical Yahoo behavior
# =========================================================
#
# dots are treated as real characters
# unlike Gmail, dots are NOT ignored
#
# johnsmith@yahoo.com
# john.smith@yahoo.com
#
# these may be treated as different accounts
#
#
# =========================================================
# Username length
# =========================================================
#
# typically practical usernames are around:
# 4 to 32 characters
#
# exact limits may vary by region and account age
#
#
# =========================================================
# Important note
# =========================================================
#
# Yahoo does not publicly expose strict complete
# validation specifications for all account types.
#
# Production systems usually use practical validation
# instead of strict RFC compliance.
#
# For library design, prefer:
# practical validation > theoretical RFC completeness
#
_YAHOO_BASE

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
#
# examples:
# .john@zohomail.com        -> invalid
# john.@zohomail.com        -> invalid
# john..smith@zohomail.com  -> invalid
#
#
# =========================================================
# Domain rules
# =========================================================
#
# domain must be valid and resolvable
# no spaces allowed
# no consecutive dots
# domain labels cannot start with hyphen (-)
# domain labels cannot end with hyphen (-)
#
# examples:
# john@-example.com         -> invalid
# john@example-.com         -> invalid
# john@example..com         -> invalid
#
#
# =========================================================
# Practical Zoho behavior
# =========================================================
#
# dots are treated as real characters
# unlike Gmail, dots are NOT ignored
#
# johnsmith@zohomail.com
# john.smith@zohomail.com
#
# these may be treated as different accounts
#
#
# =========================================================
# Important note
# =========================================================
#
# for custom domains hosted on Zoho, admin policies
# may affect what is allowed
#
# Production systems should prefer practical validation
# over strict RFC completeness
_ZOHO_BASE

#
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
#
# examples:
# .john@proton.me           -> invalid
# john.@proton.me           -> invalid
# john..smith@proton.me     -> invalid
#
#
# =========================================================
# Domain rules
# =========================================================
#
# domain must be valid and resolvable
# no spaces allowed
# no consecutive dots
# domain labels cannot start with hyphen (-)
# domain labels cannot end with hyphen (-)
#
# examples:
# john@-example.com         -> invalid
# john@example-.com         -> invalid
# john@example..com         -> invalid
#
#
# =========================================================
# Practical Proton behavior
# =========================================================
#
# dots are treated as real characters
# unlike Gmail, dots are NOT ignored
#
# johnsmith@proton.me
# john.smith@proton.me
#
# these may be treated as different accounts
#
#
# =========================================================
# Important note
# =========================================================
#
# Proton focuses heavily on privacy/security, but email
# validation rules still follow practical provider rules
# rather than full RFC edge-case support
#
# For library design, prefer:
# practical validation > theoretical RFC completeness
#
_PROTON_BASE

# SCHEME
# (?:https?|ftps?|sftp|wss?)
# What protocol is being used? Matches: http, https, ftp, ftps, sftp, ws, wss. 
# The s? means the "s" is optional — so https? matches both http and https. 
# The (?:...) is a non-capturing group — it groups the alternatives without creating a capture group.

# SEPERATOR
# ://
# Literal characters. 
# Every standard URL has :// between the scheme and the host. 
# No regex magic here — it must appear exactly as written.

# HOST ONE OF FOUR TYPES
# (?:\[IPv6\] | IPv4 | domain | localhost)
# What server are we connecting to? Four alternatives separated by |. 
# Matched in order: IPv6, IPv4, domain name, or the literal word localhost. 
# Only one needs to match.

# IPV6
# \[(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\]
# e.g. [::1] or [2001:db8::ff00]. Must be wrapped in square brackets [...]. 
# Inside: hex groups separated by colons. {0,4} means 0–4 hex digits per group. 
# {2,7} means 2 to 7 colon-separated groups — this allows compressed notation like ::.

# IPV4
# (?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)
# e.g. 192.168.1.1. Four octets separated by dots. 
# Each octet is validated to be 0–255: 25[0-5] = 250–255, 2[0-4]\d = 200–249, [01]?\d\d? = 0–199. 
# The first three octets must be followed by a dot \., 
# then the fourth octet has no trailing dot.

# DOMAIN NAME
# (?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}
# e.g. api.example.com. One or more labels separated by dots, ending with a TLD. 
# Each label: starts/ends with alphanumeric, middle can have hyphens, max 63 chars ({0,61} middle + 2 ends). 
# The + after the label group means one or more labels. TLD must be at least 2 letters [a-zA-Z]{2,}.

# Localhost
# Literal string localhost. Matches exactly the word localhost — 
# useful for local development URLs like http://localhost:3000.

# PORT
# (?::\d{1,5})?
# e.g. :8080 or :443. The ? makes it optional. 
# :\d{1,5} matches a colon followed by 1–5 digits. 
# Note: the regex allows :99999 — 
# the Python validation loop (is_valid_port) handles the 1–65535 range check separately.

# Tail — path, query, fragment (optional)
# (?:/[^\s"'<>()\[\]{}|\\^]*(?:[?#][^\s"'<>()\[\]{}|\\^]*)?)?
# Everything after the host/port. The outer (?:...)? makes it optional. 
# Structure: path starts with /, followed by any chars that are not whitespace or URL-breaking characters. 
# Then optionally a query (?...) or fragment (#...) — 
# both use the same character class. 
# The excluded chars [^\s"'<>()...] prevent the regex from swallowing 
# surrounding punctuation like closing parentheses or quotes.
_URL_STRICT_BASE