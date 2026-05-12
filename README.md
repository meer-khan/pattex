# pattex

A Python library for extracting common patterns from text using regex — emails, URLs, phone numbers, IP addresses, and more.

## Installation

```bash
pip install pattex
```

## Changelog

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



### v0.3.1 - 2026-05-13

#### Fixed

*  Zoho extractor: removed hyphen (**`-`**) and plus (**`+`**) from allowed local part
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

## Status

Currently under active development. Full documentation and usage examples coming soon.

## License

MIT
