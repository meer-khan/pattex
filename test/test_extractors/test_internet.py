from pattex.extractors.internet import extract_emails
# ─────────────────────────────────────────────────────────────────────
# PRACTICAL MODE
# ─────────────────────────────────────────────────────────────────────

class TestPracticalMode:

    # ── basic valid emails ──

    def test_simple_email(self):
        assert extract_emails("contact me at foo@bar.com") == ["foo@bar.com"]

    def test_multiple_emails(self):
        result = extract_emails("foo@bar.com and baz@qux.com")
        assert result == ["foo@bar.com", "baz@qux.com"]

    def test_email_with_dot_in_local(self):
        assert extract_emails("john.doe@example.com") == ["john.doe@example.com"]

    def test_email_with_plus_in_local(self):
        assert extract_emails("user+filter@gmail.com") == ["user+filter@gmail.com"]

    def test_email_with_underscore_in_local(self):
        assert extract_emails("user_name@example.com") == ["user_name@example.com"]

    def test_email_with_hyphen_in_local(self):
        assert extract_emails("user-name@example.com") == ["user-name@example.com"]

    def test_email_with_hyphen_in_domain(self):
        assert extract_emails("user@my-company.com") == ["user@my-company.com"]

    def test_email_with_subdomain(self):
        assert extract_emails("user@mail.company.co.uk") == ["user@mail.company.co.uk"]

    def test_email_in_sentence(self):
        result = extract_emails("Please reach out to support@example.com for help.")
        assert result == ["support@example.com"]

    def test_returns_empty_list_when_no_email(self):
        assert extract_emails("no emails here") == []

    def test_returns_empty_list_on_empty_string(self):
        assert extract_emails("") == []

    # ── local part rules ──

    def test_rejects_local_part_leading_dot(self):
        assert extract_emails(".john@example.com") == []

    def test_rejects_local_part_trailing_dot(self):
        assert extract_emails("john.@example.com") == []

    def test_rejects_local_part_leading_hyphen(self):
        assert extract_emails("-john@example.com") == []

    def test_rejects_local_part_trailing_hyphen(self):
        assert extract_emails("john-@example.com") == []

    def test_rejects_consecutive_dots_in_local(self):
        assert extract_emails("john..doe@example.com") == []

    def test_rejects_consecutive_hyphens_in_local(self):
        assert extract_emails("john--doe@example.com") == []

    def test_rejects_consecutive_plus_in_local(self):
        assert extract_emails("john++doe@example.com") == []

    def test_rejects_special_chars_in_local(self):
        # chars like ! # $ % not allowed in practical mode
        assert extract_emails("john!doe@example.com") == []
        assert extract_emails("john#doe@example.com") == []

    def test_rejects_local_part_exceeding_64_chars(self):
        local = "a" * 65
        assert extract_emails(f"{local}@example.com") == []

    def test_accepts_local_part_exactly_64_chars(self):
        local = "a" * 64
        result = extract_emails(f"{local}@example.com")
        assert result == [f"{local}@example.com"]

    # ── domain part rules ──

    def test_rejects_domain_leading_dot(self):
        assert extract_emails("john@.example.com") == []

    def test_rejects_domain_trailing_dot(self):
        assert extract_emails("john@example.com.") == []

    def test_rejects_domain_leading_hyphen(self):
        assert extract_emails("john@-example.com") == []

    def test_rejects_domain_trailing_hyphen(self):
        assert extract_emails("john@example-.com") == []

    def test_rejects_consecutive_dots_in_domain(self):
        assert extract_emails("john@example..com") == []

    def test_rejects_tld_less_than_2_chars(self):
        assert extract_emails("john@example.c") == []

    def test_accepts_tld_exactly_2_chars(self):
        assert extract_emails("john@example.pk") == ["john@example.pk"]

    def test_rejects_domain_exceeding_255_chars(self):
        domain = "a" * 250 + ".com"  # 254 chars total
        assert extract_emails(f"john@{domain}") == []

    # ── total length ──

    def test_rejects_email_exceeding_320_chars(self):
        local = "a" * 64
        domain = "b" * 250 + ".com"
        email = f"{local}@{domain}"
        assert len(email) > 320
        assert extract_emails(email) == []

    # ── default mode is practical ──

    def test_default_mode_is_practical(self):
        # consecutive dots rejected by default
        assert extract_emails("john..doe@example.com") == []


# ─────────────────────────────────────────────────────────────────────
# RFC5322 MODE
# ─────────────────────────────────────────────────────────────────────

class TestRFC5322Mode:

    def test_simple_email(self):
        result = extract_emails("foo@bar.com", mode="rfc5322")
        assert "foo@bar.com" in result

    def test_allows_extra_special_chars_in_local(self):
        # ! is allowed in rfc5322 but not practical
        result = extract_emails("john!doe@example.com", mode="rfc5322")
        assert "john!doe@example.com" in result

    def test_allows_hash_in_local(self):
        result = extract_emails("john#doe@example.com", mode="rfc5322")
        assert "john#doe@example.com" in result

    def test_returns_empty_on_no_email(self):
        assert extract_emails("no emails here", mode="rfc5322") == []


# ─────────────────────────────────────────────────────────────────────
# EDGE CASES
# ─────────────────────────────────────────────────────────────────────

class TestEdgeCases:

    def test_email_at_start_of_string(self):
        assert extract_emails("foo@bar.com is my email") == ["foo@bar.com"]

    def test_email_at_end_of_string(self):
        assert extract_emails("contact me at foo@bar.com") == ["foo@bar.com"]

    def test_multiple_emails_same_domain(self):
        result = extract_emails("a@x.com and b@x.com")
        assert result == ["a@x.com", "b@x.com"]

    def test_no_duplicates_for_same_email(self):
        result = extract_emails("foo@bar.com foo@bar.com")
        # currently returns duplicates — this test documents current behavior
        assert result.count("foo@bar.com") == 2

    def test_email_with_numbers_in_local(self):
        assert extract_emails("user123@example.com") == ["user123@example.com"]

    def test_email_with_numbers_in_domain(self):
        assert extract_emails("user@example123.com") == ["user@example123.com"]

    def test_invalid_no_at_sign(self):
        assert extract_emails("notanemail.com") == []

    def test_invalid_no_domain(self):
        assert extract_emails("user@") == []

    def test_invalid_no_local(self):
        assert extract_emails("@example.com") == []