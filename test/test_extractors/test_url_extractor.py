

# -------------------------------------   TEST URLS ----------------------------------------------------------------

"""
Tests for URL extraction functions in pattex.extractors.url_extractor.

Run with: pytest test/test_extractors/test_urls_extractor.py -v
"""
from pattex.extractors.urls_extraction import (
    extract_urls,
    extract_urls_by_scheme,
    extract_urls_by_domain,
)

# ─────────────────────────────────────────────────────────────────────────────
# extract_urls — strict mode (default)
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractUrlsStrict:

    def test_simple_https(self):
        text = "Visit https://example.com for details."
        assert extract_urls(text) == ["https://example.com"]

    def test_simple_http(self):
        text = "Go to http://example.com/page"
        assert extract_urls(text) == ["http://example.com/page"]

    def test_multiple_urls(self):
        text = "See https://foo.com and https://bar.org/path"
        result = extract_urls(text)
        assert "https://foo.com" in result
        assert "https://bar.org/path" in result
        assert len(result) == 2

    def test_url_with_path(self):
        text = "https://api.example.com/v1/users/123"
        assert extract_urls(text) == ["https://api.example.com/v1/users/123"]

    def test_url_with_query(self):
        text = "https://search.example.com/results?q=hello+world&page=2"
        assert "q=hello+world" in extract_urls(text)[0]

    def test_url_with_fragment(self):
        text = "https://docs.example.com/guide#section-3"
        assert extract_urls(text) == ["https://docs.example.com/guide#section-3"]

    def test_url_with_port(self):
        text = "Service at https://api.example.com:8443/endpoint"
        assert extract_urls(text) == ["https://api.example.com:8443/endpoint"]

    def test_invalid_port_rejected(self):
        text = "https://example.com:99999/path"
        assert extract_urls(text) == []

    def test_url_with_credentials(self):
        text = "ftp://user:secret@ftp.example.com/files"
        result = extract_urls(text)
        assert len(result) == 1
        assert "ftp.example.com" in result[0]

    def test_ftp_scheme(self):
        text = "Download from ftp://files.example.com/archive.tar.gz"
        result = extract_urls(text)
        assert len(result) == 1
        assert result[0].startswith("ftp://")

    def test_ftps_scheme(self):
        assert extract_urls("ftps://secure.example.com/data") == ["ftps://secure.example.com/data"]

    def test_sftp_scheme(self):
        assert extract_urls("sftp://deploy@server.example.com/var/www") != []

    def test_ws_scheme(self):
        assert extract_urls("ws://realtime.example.com/socket") == ["ws://realtime.example.com/socket"]

    def test_wss_scheme(self):
        assert extract_urls("wss://realtime.example.com/socket") == ["wss://realtime.example.com/socket"]

    def test_ipv4_url(self):
        text = "http://192.168.1.1/admin"
        assert extract_urls(text) == ["http://192.168.1.1/admin"]

    def test_ipv4_with_port(self):
        text = "http://10.0.0.1:8080/dashboard"
        assert extract_urls(text) == ["http://10.0.0.1:8080/dashboard"]

    def test_ipv6_url(self):
        text = "http://[2001:db8::1]/path"
        result = extract_urls(text)
        assert len(result) == 1

    def test_subdomain(self):
        text = "https://api.v2.example.com/resource"
        assert extract_urls(text) == ["https://api.v2.example.com/resource"]

    def test_trailing_dot_stripped(self):
        text = "See https://example.com."
        assert extract_urls(text) == ["https://example.com"]

    def test_trailing_comma_stripped(self):
        text = "Visit https://example.com, then proceed."
        assert extract_urls(text) == ["https://example.com"]

    def test_trailing_paren_stripped(self):
        text = "Link (https://example.com)"
        assert extract_urls(text) == ["https://example.com"]

    def test_url_in_quotes_stripped(self):
        text = 'href="https://example.com/page"'
        assert extract_urls(text) == ["https://example.com/page"]

    def test_url_in_angle_brackets_stripped(self):
        text = "See <https://example.com/page>"
        assert extract_urls(text) == ["https://example.com/page"]

    def test_markdown_link(self):
        text = "[Click here](https://example.com/page)"
        assert extract_urls(text) == ["https://example.com/page"]

    def test_deduplication(self):
        text = "https://example.com and again https://example.com"
        assert extract_urls(text) == ["https://example.com"]

    def test_host_lowercased(self):
        text = "https://Example.COM/Path/To/Resource"
        result = extract_urls(text)
        assert result[0].startswith("https://example.com/")
        # path case preserved
        assert "/Path/To/Resource" in result[0]

    def test_bare_domain_not_matched_in_strict(self):
        text = "example.com/path"
        assert extract_urls(text) == []

    def test_localhost_not_matched_by_default(self):
        text = "Running on localhost:8000/api"
        assert extract_urls(text) == []

    def test_localhost_included_when_flag_set(self):
        text = "Running on localhost:8000/api"
        result = extract_urls(text, include_localhost=True)
        assert len(result) == 1
        assert "localhost" in result[0]

    def test_schemed_localhost_always_matched(self):
        text = "http://localhost:5000/dashboard"
        assert extract_urls(text) == ["http://localhost:5000/dashboard"]

    def test_no_urls_returns_empty(self):
        text = "No URLs in this sentence at all."
        assert extract_urls(text) == []

    def test_email_not_matched(self):
        text = "Contact us at hello@example.com"
        assert extract_urls(text) == []

    def test_version_string_not_matched(self):
        text = "Version 1.2.3 is released."
        assert extract_urls(text) == []

    def test_multiple_schemes_in_text(self):
        text = "https://example.com ws://socket.io ftp://files.org"
        result = extract_urls(text)
        assert len(result) == 3

    def test_url_with_complex_query(self):
        text = "https://example.com/search?q=foo+bar&sort=desc&page=1#results"
        result = extract_urls(text)
        assert len(result) == 1
        assert "q=foo+bar" in result[0]
        assert "#results" in result[0]


# ─────────────────────────────────────────────────────────────────────────────
# extract_urls — permissive mode
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractUrlsPermissive:

    def test_bare_domain_with_known_tld(self):
        text = "Visit example.com for more info."
        result = extract_urls(text, mode="permissive")
        assert any("example.com" in u for u in result)

    def test_bare_domain_with_www(self):
        text = "Go to www.example.com/page"
        result = extract_urls(text, mode="permissive")
        assert any("example.com" in u for u in result)

    def test_bare_domain_unknown_tld_rejected(self):
        text = "example.invalidtld/path"
        result = extract_urls(text, mode="permissive")
        assert not any("invalidtld" in u for u in result)

    def test_protocol_relative(self):
        text = "src='//cdn.example.com/script.js'"
        result = extract_urls(text, mode="permissive")
        assert any("cdn.example.com" in u for u in result)

    def test_bare_ipv4(self):
        text = "Server at 192.168.1.100:9000/health"
        result = extract_urls(text, mode="permissive")
        assert any("192.168.1.100" in u for u in result)

    def test_localhost_in_permissive(self):
        text = "localhost:3000/api/users"
        result = extract_urls(text, mode="permissive")
        assert any("localhost" in u for u in result)

    def test_schemed_urls_still_captured(self):
        text = "https://example.com and also example.org"
        result = extract_urls(text, mode="permissive")
        assert any("https://example.com" in u for u in result)
        assert any("example.org" in u for u in result)

    def test_email_not_captured_as_bare_domain(self):
        text = "user@example.com"
        result = extract_urls(text, mode="permissive")
        # the domain part of an email must not appear as a bare URL
        assert not any(u == "example.com" or u.endswith("/example.com") for u in result)

    def test_dedup_across_strict_and_permissive_layers(self):
        # https://example.com caught by strict; example.com by permissive bare —
        # they should not be returned as two separate entries
        text = "https://example.com and also example.com"
        result = extract_urls(text, mode="permissive")
        assert len([u for u in result if "example.com" in u and "https" in u]) == 1


# ─────────────────────────────────────────────────────────────────────────────
# extract_urls_by_scheme
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractUrlsByScheme:

    def test_https_only(self):
        text = "https://secure.com http://insecure.com ftp://files.com"
        result = extract_urls_by_scheme(text, "https")
        assert all(u.startswith("https://") for u in result)
        assert len(result) == 1

    def test_http_only(self):
        text = "https://secure.com http://insecure.com"
        result = extract_urls_by_scheme(text, "http")
        assert result == ["http://insecure.com"]

    def test_ftp(self):
        text = "ftp://files.example.com/data.zip"
        assert extract_urls_by_scheme(text, "ftp") == ["ftp://files.example.com/data.zip"]

    def test_wss(self):
        text = "Connect to wss://realtime.example.com/ws"
        result = extract_urls_by_scheme(text, "wss")
        assert len(result) == 1
        assert result[0].startswith("wss://")

    def test_no_match_returns_empty(self):
        text = "https://example.com"
        assert extract_urls_by_scheme(text, "ftp") == []

    def test_deduplication(self):
        text = "https://example.com https://example.com"
        assert extract_urls_by_scheme(text, "https") == ["https://example.com"]

    def test_invalid_port_rejected(self):
        text = "https://example.com:99999/path"
        assert extract_urls_by_scheme(text, "https") == []


# ─────────────────────────────────────────────────────────────────────────────
# extract_urls_by_domain
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractUrlsByDomain:

    def test_exact_domain(self):
        text = "https://example.com/page and https://other.com/page"
        result = extract_urls_by_domain(text, "example.com")
        assert all("example.com" in u for u in result)
        assert len(result) == 1

    def test_subdomains_included(self):
        text = "https://api.example.com/v1 https://www.example.com https://example.com"
        result = extract_urls_by_domain(text, "example.com")
        assert len(result) == 3

    def test_similar_domain_not_matched(self):
        text = "https://notexample.com/page https://example.com.evil.com"
        result = extract_urls_by_domain(text, "example.com")
        assert result == []

    def test_case_insensitive_domain(self):
        text = "https://Example.COM/page"
        result = extract_urls_by_domain(text, "example.com")
        assert len(result) == 1

    def test_no_match_returns_empty(self):
        text = "https://other.com/page"
        assert extract_urls_by_domain(text, "example.com") == []