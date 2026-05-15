## Changelog


### [0.4.0] - 2026-05-16

#### Added

**`url_extractor.py`**

* `extract_urls_by_scheme(text, scheme)` — filter URLs by a specific scheme
* `extract_urls_by_domain(text, domain, include_subdomains)` — filter URLs by domain, with optional subdomain matching
* `extract_urls_by_tld(text, tld)` — filter URLs by TLD, leading dot optional
* `extract_secure_urls(text)` — returns only https, ftps, sftp, wss URLs
* `extract_insecure_urls(text)` — returns only http, ftp, ws URLs
* `extract_urls_with_auth(text)` — returns only URLs containing userinfo (`user:pass@host`)
* `extract_urls_with_port(text, port)` — returns URLs with any port, or a specific port
* `extract_unique_domains(text, root_only)` — unique hostnames or root domains across all URLs
* `is_url(text, strict)` — validates whether a string is a valid URL
* `allow_ipv4`, `allow_ipv6`, `allow_port`, `allow_tail`, `schemes` parameters added to `extract_urls`
* `_build_strict_regex()` — dynamic regex builder with `lru_cache(maxsize=16)`
* `_build_permissive_regex()` — single combined permissive regex with named groups, `lru_cache(maxsize=1)`

**`ip_extractor.py`** ← new file

* `extract_ip_urls(text, ipv4, ipv6)` — extract URLs whose host is an IP address
* `extract_localhost_urls(text, allow_port, allow_tail)` — extract localhost URLs only

**`regexes.py`**

* `_SCHEMES` — raw scheme alternation string
* `_BARE_DOMAIN` — raw bare domain pattern without port/tail

**`_utils.py`**

* `_get_root_domain(host)` — extracts root domain from hostname
* `has_auth(url)` — checks whether a URL contains userinfo
* `_is_ip_host(url)` — checks whether a URL host is an IP address

**`extractor_constants.py`**

* `URL_SCHEMES` — `Literal` type for all supported schemes

#### Changed

* `include_localhost` renamed to `allow_localhost` — **breaking change**
* Permissive mode now runs a **single `finditer` scan** instead of 3–4 separate loops — protocol-relative, bare domain, bare IP, and localhost combined into one regex via named groups (`(?P<name>...)`)
* `match.lastgroup` used to dispatch per-branch guard logic in permissive loop
* Localhost always included in permissive mode implicitly — `allow_localhost` only controls strict mode
* `_build_permissive_regex` takes no arguments — localhost always included in permissive
* Schemed `http://localhost` always extracted in strict mode regardless of `allow_localhost`
* `extract_secure_urls` and `extract_insecure_urls` have no `mode` parameter — scheme implies strictness

#### Internal

* All raw pattern constants kept as plain strings in `regexes.py` — compiled only at assembly time
* `lru_cache` on both builders avoids recompilation on repeated calls with same flags
* `urlparse` import consolidated at top of `url_extractor.py`
* Walrus operator used in `extract_urls_with_port` to avoid double `urlparse` call


### v0.3.1 - 2026-05-13

#### Fixed

* Zoho extractor: removed hyphen (**`-`**) and plus (**`+`**) from allowed local part
  characters — Zoho usernames only permit letters, numbers, dots, and
  underscores per official documentation
* Zoho extractor: **`+`** is a subaddressing tag separator, not a valid account
  creation character; removed from base regex and validation logic
* Proton extractor: tightened leading/trailing character rule — local part must
  begin and end with an alphanumeric character (was checking against **`._-`** set,
  now explicitly uses **`isalnum()`** to match Proton's documented rule)

#### Changed

* Renamed **`email_extraction.py`** → **`email_extractor.py`**
* Renamed **`urls_extraction.py`** → **`url_extractor.py`**
* Updated docstrings for **`extract_zoho_emails`** and **`extract_proton_emails`** to
  reflect corrected provider rules
* Added inline comments on each validation rule inside **`email_extractor.py`** for
  all six provider extractors
* Added documentation comments for all email regex patterns in
  **`constants/regexes.py`** and corresponding **`.pyi`** stubs

#### Internal

* General code cleanups across extractor modules

### v0.3.0

**pattex v0.3.0** brings a significant internal restructuring alongside new features and bug fixes.

---

**Breaking / Structural**

* `internet.py` has been split into `email_extractor.py` and `url_extractor.py`. If you were importing directly from the internal module path, update your imports. Top-level `pattex` imports are unaffected.

**New Features**

* **URL Extraction** — `extract_urls(text, mode)`, `extract_urls_by_scheme(text, scheme)`, and `extract_urls_by_domain(text, domain)` are now available. Supports strict and permissive modes covering HTTP/S, FTP, WebSocket, IPv4, IPv6, bare domains, and localhost.
* **Gmail normalisation** — `extract_gmail_emails` now accepts `normalize=True` which strips dots from the local part, unifies `@googlemail.com` to `@gmail.com`, and deduplicates canonical variants.
* **`is_valid_provider_email(email, provider)`** — single function to validate whether an email belongs to a given provider (`gmail`, `yahoo`, `outlook`, `icloud`, `zoho`, `proton`).

**Bug Fixes**

* Fixed `extract_emails_by_provider` which was not dispatching to provider helper functions correctly — all six providers now route properly.
