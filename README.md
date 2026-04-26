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

## Status

Currently under active development. Full documentation and usage examples coming soon.

## License

MIT
