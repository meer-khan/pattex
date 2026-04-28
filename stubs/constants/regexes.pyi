from pattex.constants.regexes import _OUTLOOK_BASE, _ICLOUD_BASE, _ZOHO_BASE, _PROTON_BASE, _GMAIL_BASE, _YAHOO_BASE

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