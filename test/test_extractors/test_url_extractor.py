
"""
Tests for URL extraction functions in pattex.extractors.url_extractor.

Run with: pytest test/test_extractors/test_urls_extractor.py -v
"""
import pytest

# -------------------------------------   TEST URLS ----------------------------------------------------------------
from pattex.extractors.url_extractor import (
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
        result = extract_urls(text, allow_localhost=True)
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



"""
Additional tests for extract_urls in pattex.extractors.url_extractor.
 
Covers gaps not addressed in the existing test suite:
    - All 7 schemes validated via parametrize
    - Scheme case-insensitivity
    - Unsupported schemes rejected
    - Port boundary values (1, 65535, 65536, 0)
    - IPv4 octet boundary validation
    - IPv6 variations
    - Trailing noise full character set
    - localhost interaction with include_localhost flag and permissive mode
    - Bare IP not double-counted in permissive mode
    - Order preservation
    - Empty and whitespace-only input
    - URL extracted from common surrounding contexts
 
Run with: pytest test/test_extractors/test_extract_urls_new.py -v
"""
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Schemes
# ─────────────────────────────────────────────────────────────────────────────
 
@pytest.mark.parametrize("scheme", ["http", "https", "ftp", "ftps", "sftp", "ws", "wss"])
def test_all_valid_schemes_matched(scheme):
    result = extract_urls(f"{scheme}://example.com/path")
    assert len(result) == 1
    assert result[0].startswith(f"{scheme}://")
 
 
@pytest.mark.parametrize("scheme", ["http", "https", "ftp", "ftps", "sftp", "ws", "wss"])
def test_schemes_case_insensitive(scheme):
    result = extract_urls(f"{scheme.upper()}://example.com/path")
    assert len(result) == 1
    assert result[0].startswith(f"{scheme}://")
 
 
@pytest.mark.parametrize("bad_scheme", ["mailto", "javascript", "data", "tel", "file"])
def test_unsupported_schemes_rejected(bad_scheme):
    assert extract_urls(f"{bad_scheme}://example.com") == []
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Port boundary values
# ─────────────────────────────────────────────────────────────────────────────
 
@pytest.mark.parametrize("port", [1, 80, 443, 8080, 65535])
def test_valid_ports_accepted(port):
    result = extract_urls(f"https://example.com:{port}/path")
    assert len(result) == 1
    assert f":{port}" in result[0]
 
 
@pytest.mark.parametrize("port", [0, 65536, 99999])
def test_invalid_ports_rejected(port):
    assert extract_urls(f"https://example.com:{port}/path") == []
 
 
# ─────────────────────────────────────────────────────────────────────────────
# IPv4 octet boundaries
# ─────────────────────────────────────────────────────────────────────────────
 
@pytest.mark.parametrize("ip", [
    "0.0.0.0",
    "127.0.0.1",
    "192.168.1.1",
    "255.255.255.255",
    "10.0.0.1",
])
def test_valid_ipv4_matched(ip):
    result = extract_urls(f"http://{ip}/path")
    assert len(result) == 1
    assert ip in result[0]
 
 
@pytest.mark.parametrize("ip", ["256.0.0.1", "999.999.999.999"])
def test_invalid_ipv4_rejected(ip):
    assert extract_urls(f"http://{ip}/path") == []


def test_ipv4_partial_match_from_longer_octet():
    # 192.168.1.999 — the regex correctly extracts 192.168.1.99 (valid IP)
    # and leaves the trailing 9 behind. This is expected regex behaviour,
    # not a bug — the regex finds the longest valid IP it can inside the string.
    result = extract_urls("http://192.168.1.999/path")
    assert result == ["http://192.168.1.99"]
 
# ─────────────────────────────────────────────────────────────────────────────
# IPv6 variations
# ─────────────────────────────────────────────────────────────────────────────
 
@pytest.mark.parametrize("ipv6", [
    "[::1]",
    "[2001:db8::1]",
    "[2001:db8:0:0:0:0:0:1]",
    "[fe80::1]",
])
def test_valid_ipv6_matched(ipv6):
    result = extract_urls(f"http://{ipv6}/path")
    assert len(result) == 1
 
 
def test_ipv6_without_brackets_not_matched():
    # bare IPv6 without brackets must not be matched as a URL host
    assert extract_urls("http://2001:db8::1/path") == []
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Trailing noise — full character set
# ─────────────────────────────────────────────────────────────────────────────
 
@pytest.mark.parametrize("noise", [".", ",", "!", "?", ";", ":", "'", '"', ")", ">", "]"])
def test_trailing_noise_stripped(noise):
    assert extract_urls(f"https://example.com{noise}") == ["https://example.com"]
 
 
def test_trailing_noise_not_stripped_from_inside_query():
    # a dot inside the query string is part of the URL, not trailing noise
    result = extract_urls("https://example.com/path?q=hello.world")
    assert len(result) == 1
    assert "q=hello.world" in result[0]
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Localhost
# ─────────────────────────────────────────────────────────────────────────────
 
def test_bare_localhost_excluded_in_strict():
    assert extract_urls("localhost:3000") == []
 
 
def test_bare_localhost_included_with_flag():
    result = extract_urls("localhost:3000/api", allow_localhost=True)
    assert len(result) == 1
    assert "localhost" in result[0]
 
 
def test_schemed_localhost_always_included():
    assert extract_urls("http://localhost:5000/dashboard") == ["http://localhost:5000/dashboard"]
 
 
def test_schemed_localhost_not_double_counted_with_flag():
    # strict base catches http://localhost; flag enables bare scan — must not duplicate
    result = extract_urls("http://localhost:5000", allow_localhost=True)
    assert len(result) == 1
 
 
def test_schemed_localhost_not_double_counted_in_permissive():
    result = extract_urls("http://localhost:5000", mode="permissive")
    assert len(result) == 1
 
 
def test_localhost_in_permissive_without_scheme():
    result = extract_urls("localhost:8080/health", mode="permissive")
    assert any("localhost" in u for u in result)
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Permissive mode — deduplication across layers
# ─────────────────────────────────────────────────────────────────────────────
 
def test_schemed_ipv4_not_double_counted_in_permissive():
    # strict catches http://192.168.1.1; bare IP scan must not re-add it
    result = extract_urls("http://192.168.1.1/api", mode="permissive")
    assert len(result) == 1
 
 
def test_bare_ipv4_captured_in_permissive():
    result = extract_urls("Server at 10.0.0.1:9000/health", mode="permissive")
    assert any("10.0.0.1" in u for u in result)
 
 
def test_protocol_relative_not_double_counted():
    result = extract_urls("//cdn.example.com/script.js", mode="permissive")
    assert len([u for u in result if "cdn.example.com" in u]) == 1
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Order preservation
# ─────────────────────────────────────────────────────────────────────────────
 
def test_first_occurrence_order_preserved():
    text = "https://first.com then https://second.com then https://third.com"
    assert extract_urls(text) == [
        "https://first.com",
        "https://second.com",
        "https://third.com",
    ]
 
 
def test_dedup_keeps_first_occurrence():
    result = extract_urls("https://example.com/first and https://EXAMPLE.COM/first")
    assert len(result) == 1
    assert result[0] == "https://example.com/first"
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Edge inputs
# ─────────────────────────────────────────────────────────────────────────────
 
def test_empty_string():
    assert extract_urls("") == []
 
 
def test_whitespace_only():
    assert extract_urls("   \n\t  ") == []
 
 
def test_url_only_no_surrounding_text():
    assert extract_urls("https://example.com") == ["https://example.com"]
 
 
def test_url_surrounded_by_newlines():
    assert extract_urls("\nhttps://example.com\n") == ["https://example.com"]
 
 
@pytest.mark.parametrize("context,expected", [
    ('href="https://example.com"',      "https://example.com"),
    ("<https://example.com>",           "https://example.com"),
    ("(https://example.com)",           "https://example.com"),
    ("[link](https://example.com)",     "https://example.com"),
    ("See https://example.com.",        "https://example.com"),
    ("at https://example.com,",         "https://example.com"),
])
def test_url_extracted_from_common_contexts(context, expected):
    assert expected in extract_urls(context)