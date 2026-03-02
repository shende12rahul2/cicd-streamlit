"""Unit tests for src.validation — input validation helpers."""

from __future__ import annotations

from src.validation import (
    validate_file_extension,
    validate_file_size,
    validate_row_count_input,
    validate_search_term,
)

# ── Tests for validate_file_extension ──────────────────────────────


class TestValidateFileExtension:
    """Tests for validate_file_extension."""

    def test_valid_csv(self) -> None:
        """Should accept .csv files."""
        is_valid, _ = validate_file_extension("data.csv")
        assert is_valid is True

    def test_valid_csv_uppercase(self) -> None:
        """Should accept .CSV (case-insensitive)."""
        is_valid, _ = validate_file_extension("DATA.CSV")
        assert is_valid is True

    def test_invalid_extension(self) -> None:
        """Should reject non-CSV extensions."""
        is_valid, msg = validate_file_extension("data.xlsx")
        assert is_valid is False
        assert "Invalid" in msg

    def test_empty_filename(self) -> None:
        """Should reject empty filenames."""
        is_valid, _ = validate_file_extension("")
        assert is_valid is False

    def test_no_extension(self) -> None:
        """Should reject files with no extension."""
        is_valid, _ = validate_file_extension("noextension")
        assert is_valid is False

    def test_multiple_dots(self) -> None:
        """Should handle filenames with multiple dots."""
        is_valid, _ = validate_file_extension("my.data.file.csv")
        assert is_valid is True


# ── Tests for validate_file_size ───────────────────────────────────


class TestValidateFileSize:
    """Tests for validate_file_size."""

    def test_valid_size(self) -> None:
        """Should accept a reasonable file size."""
        is_valid, _ = validate_file_size(1024)
        assert is_valid is True

    def test_zero_size(self) -> None:
        """Should reject zero-byte files."""
        is_valid, _ = validate_file_size(0)
        assert is_valid is False

    def test_negative_size(self) -> None:
        """Should reject negative sizes."""
        is_valid, _ = validate_file_size(-100)
        assert is_valid is False

    def test_too_large(self) -> None:
        """Should reject files exceeding the limit."""
        is_valid, msg = validate_file_size(100 * 1024 * 1024)
        assert is_valid is False
        assert "exceeds" in msg

    def test_exactly_at_limit(self) -> None:
        """Should accept files exactly at the limit."""
        is_valid, _ = validate_file_size(50 * 1024 * 1024)
        assert is_valid is True

    def test_message_includes_size(self) -> None:
        """Message should include the file size in MB."""
        _, msg = validate_file_size(1024 * 1024)
        assert "1.00 MB" in msg


# ── Tests for validate_row_count_input ─────────────────────────────


class TestValidateRowCountInput:
    """Tests for validate_row_count_input."""

    def test_valid_input(self) -> None:
        """Should accept a valid integer string."""
        is_valid, n, _ = validate_row_count_input("10")
        assert is_valid is True
        assert n == 10

    def test_non_integer(self) -> None:
        """Should reject non-numeric input."""
        is_valid, _, _ = validate_row_count_input("abc")
        assert is_valid is False

    def test_negative(self) -> None:
        """Should reject negative values."""
        is_valid, _, _ = validate_row_count_input("-5")
        assert is_valid is False

    def test_zero(self) -> None:
        """Should reject zero."""
        is_valid, _, _ = validate_row_count_input("0")
        assert is_valid is False

    def test_too_large(self) -> None:
        """Should reject values exceeding the maximum."""
        is_valid, _, _ = validate_row_count_input("999999")
        assert is_valid is False

    def test_empty_string(self) -> None:
        """Should reject empty input."""
        is_valid, _, _ = validate_row_count_input("")
        assert is_valid is False

    def test_whitespace_only(self) -> None:
        """Should reject whitespace-only input."""
        is_valid, _, _ = validate_row_count_input("   ")
        assert is_valid is False

    def test_leading_trailing_spaces(self) -> None:
        """Should accept input with leading/trailing whitespace."""
        is_valid, n, _ = validate_row_count_input("  42  ")
        assert is_valid is True
        assert n == 42

    def test_float_string(self) -> None:
        """Should reject float values."""
        is_valid, _, _ = validate_row_count_input("3.5")
        assert is_valid is False


# ── Tests for validate_search_term ─────────────────────────────────


class TestValidateSearchTerm:
    """Tests for validate_search_term."""

    def test_valid_term(self) -> None:
        """Should accept a normal search term."""
        is_valid, _ = validate_search_term("hello")
        assert is_valid is True

    def test_empty_term(self) -> None:
        """Should reject empty strings."""
        is_valid, _ = validate_search_term("")
        assert is_valid is False

    def test_whitespace_only(self) -> None:
        """Should reject whitespace-only input."""
        is_valid, _ = validate_search_term("   ")
        assert is_valid is False

    def test_too_long(self) -> None:
        """Should reject terms exceeding max length."""
        is_valid, msg = validate_search_term("x" * 201)
        assert is_valid is False
        assert "too long" in msg

    def test_special_characters(self) -> None:
        """Should accept terms with special characters."""
        is_valid, _ = validate_search_term("hello@world#123")
        assert is_valid is True

    def test_unicode_term(self) -> None:
        """Should accept unicode search terms."""
        is_valid, _ = validate_search_term("München")
        assert is_valid is True
