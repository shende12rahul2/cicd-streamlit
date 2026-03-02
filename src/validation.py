"""Input validation helpers for the Streamlit CSV Analyzer.

All validation logic is kept here so the UI layer stays clean.
Constants are imported from ``src.config`` for single-source-of-truth.
"""

from __future__ import annotations

from src.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    MAX_PREVIEW_ROWS,
    MAX_SEARCH_TERM_LENGTH,
)


def validate_file_extension(filename: str) -> tuple[bool, str]:
    """Validate that the uploaded file has an allowed extension.

    Args:
        filename: The name of the uploaded file.

    Returns:
        A tuple of (is_valid, message).
    """
    if not filename:
        return False, "No file name provided."

    extension = (
        "." + filename.rsplit(".", maxsplit=1)[-1].lower() if "." in filename else ""
    )
    if extension not in ALLOWED_EXTENSIONS:
        return False, (
            f"Invalid file type '{extension}'. "
            f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    return True, "File extension is valid."


def validate_file_size(size_bytes: int) -> tuple[bool, str]:
    """Validate that the uploaded file does not exceed the size limit.

    Args:
        size_bytes: File size in bytes.

    Returns:
        A tuple of (is_valid, message).
    """
    if size_bytes <= 0:
        return False, "File appears to be empty (0 bytes)."

    size_mb = size_bytes / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, (
            f"File size ({size_mb:.1f} MB) exceeds the " f"{MAX_FILE_SIZE_MB} MB limit."
        )
    return True, f"File size ({size_mb:.2f} MB) is within the limit."


def validate_row_count_input(value: str) -> tuple[bool, int, str]:
    """Validate the user-provided row count for preview.

    Args:
        value: Raw string from the text input.

    Returns:
        A tuple of (is_valid, parsed_value, message).
    """
    if not value or not value.strip():
        return False, 0, "Please enter a number of rows."

    try:
        n = int(value.strip())
    except ValueError:
        return False, 0, f"'{value}' is not a valid integer."

    if n <= 0:
        return False, 0, "Number of rows must be a positive integer."
    if n > MAX_PREVIEW_ROWS:
        return False, 0, f"Maximum preview is {MAX_PREVIEW_ROWS:,} rows."

    return True, n, f"Will display {n} rows."


def validate_search_term(term: str) -> tuple[bool, str]:
    """Validate a search/filter term.

    Args:
        term: The search string entered by the user.

    Returns:
        A tuple of (is_valid, message).
    """
    if not term or not term.strip():
        return False, "Search term cannot be empty."
    if len(term) > MAX_SEARCH_TERM_LENGTH:
        return False, (
            f"Search term is too long (max {MAX_SEARCH_TERM_LENGTH} characters)."
        )
    return True, "Search term is valid."
