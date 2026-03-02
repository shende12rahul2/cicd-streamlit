"""Shared test fixtures for the CSV Data Analyzer test suite."""

from __future__ import annotations

import io

import pandas as pd
import pytest


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    """Return a small sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
            "age": [30, 25, 35, 28, 32],
            "salary": [70000, 55000, 90000, 62000, 78000],
            "department": [
                "Engineering",
                "Marketing",
                "Engineering",
                "Sales",
                "Marketing",
            ],
        }
    )


@pytest.fixture()
def csv_bytes() -> bytes:
    """Return raw CSV bytes for testing load_csv."""
    return b"name,age\nAlice,30\nBob,25\n"


@pytest.fixture()
def csv_file(csv_bytes: bytes) -> io.BytesIO:
    """Return a file-like CSV object."""
    return io.BytesIO(csv_bytes)


@pytest.fixture()
def large_df() -> pd.DataFrame:
    """Return a larger DataFrame for edge-case testing."""
    return pd.DataFrame(
        {
            "id": range(1, 1001),
            "value": [float(i) * 1.5 for i in range(1, 1001)],
            "category": [f"cat_{i % 10}" for i in range(1, 1001)],
        }
    )


@pytest.fixture()
def df_with_nulls() -> pd.DataFrame:
    """Return a DataFrame containing null values."""
    return pd.DataFrame(
        {
            "name": ["Alice", None, "Charlie"],
            "score": [95.0, None, 78.5],
        }
    )
