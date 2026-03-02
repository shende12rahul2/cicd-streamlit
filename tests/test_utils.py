"""Unit tests for src.utils — data loading and processing."""

from __future__ import annotations

import io

import pandas as pd
import pytest

from src.utils import (
    filter_dataframe,
    get_column_info,
    get_numeric_columns,
    get_summary_statistics,
    get_top_n_rows,
    load_csv,
)

# ── Tests for load_csv ─────────────────────────────────────────────


class TestLoadCsv:
    """Tests for the load_csv function."""

    def test_load_valid_csv(self, csv_bytes: bytes) -> None:
        """Should successfully load a valid CSV."""
        df = load_csv(io.BytesIO(csv_bytes))
        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]

    def test_load_empty_csv_raises(self) -> None:
        """Should raise ValueError for an empty file."""
        with pytest.raises(ValueError, match="empty"):
            load_csv(io.BytesIO(b""))

    def test_load_header_only_csv_raises(self) -> None:
        """Should raise ValueError when CSV has headers but no data rows."""
        with pytest.raises(ValueError, match="no data rows"):
            load_csv(io.BytesIO(b"col1,col2\n"))

    def test_load_csv_with_special_characters(self) -> None:
        """Should handle CSV containing unicode and special chars."""
        data = "name,city\nÉlise,São Paulo\nMüller,Zürich\n".encode()
        df = load_csv(io.BytesIO(data))
        assert len(df) == 2
        assert df.iloc[0]["name"] == "Élise"


# ── Tests for get_summary_statistics ───────────────────────────────


class TestGetSummaryStatistics:
    """Tests for the get_summary_statistics function."""

    def test_returns_stats_for_numeric_columns(self, sample_df: pd.DataFrame) -> None:
        """Should return describe() output for numeric columns."""
        stats = get_summary_statistics(sample_df)
        assert "age" in stats.columns
        assert "salary" in stats.columns
        assert "name" not in stats.columns

    def test_no_numeric_columns(self) -> None:
        """Should return info message when there are no numeric columns."""
        df = pd.DataFrame({"a": ["x", "y"], "b": ["p", "q"]})
        stats = get_summary_statistics(df)
        assert "info" in stats.columns

    def test_stats_include_standard_rows(self, sample_df: pd.DataFrame) -> None:
        """Should include count, mean, std, min, max in output."""
        stats = get_summary_statistics(sample_df)
        expected_index = {"count", "mean", "std", "min", "max"}
        assert expected_index.issubset(set(stats.index))


# ── Tests for get_column_info ──────────────────────────────────────


class TestGetColumnInfo:
    """Tests for the get_column_info function."""

    def test_column_info_shape(self, sample_df: pd.DataFrame) -> None:
        """Should return one row per column."""
        info = get_column_info(sample_df)
        assert len(info) == len(sample_df.columns)
        assert "Column" in info.columns
        assert "Null Count" in info.columns

    def test_null_counts_with_nulls(self, df_with_nulls: pd.DataFrame) -> None:
        """Should correctly report null counts."""
        info = get_column_info(df_with_nulls)
        name_row = info[info["Column"] == "name"].iloc[0]
        assert name_row["Null Count"] == 1


# ── Tests for filter_dataframe ─────────────────────────────────────


class TestFilterDataframe:
    """Tests for the filter_dataframe function."""

    def test_filter_matches(self, sample_df: pd.DataFrame) -> None:
        """Should return rows matching the search term."""
        result = filter_dataframe(sample_df, "department", "Engineering")
        assert len(result) == 2

    def test_filter_case_insensitive(self, sample_df: pd.DataFrame) -> None:
        """Search should be case-insensitive."""
        result = filter_dataframe(sample_df, "name", "alice")
        assert len(result) == 1

    def test_filter_no_match(self, sample_df: pd.DataFrame) -> None:
        """Should return empty DataFrame when nothing matches."""
        result = filter_dataframe(sample_df, "name", "Zara")
        assert result.empty

    def test_filter_invalid_column(self, sample_df: pd.DataFrame) -> None:
        """Should raise KeyError for a non-existent column."""
        with pytest.raises(KeyError, match="not_a_column"):
            filter_dataframe(sample_df, "not_a_column", "x")

    def test_filter_partial_match(self, sample_df: pd.DataFrame) -> None:
        """Should match partial substrings."""
        result = filter_dataframe(sample_df, "name", "li")
        assert len(result) == 2  # Alice, Charlie


# ── Tests for get_numeric_columns ──────────────────────────────────


class TestGetNumericColumns:
    """Tests for the get_numeric_columns function."""

    def test_returns_numeric_only(self, sample_df: pd.DataFrame) -> None:
        """Should only include numeric column names."""
        cols = get_numeric_columns(sample_df)
        assert "age" in cols
        assert "salary" in cols
        assert "name" not in cols

    def test_empty_for_non_numeric(self) -> None:
        """Should return empty list when no numeric columns exist."""
        df = pd.DataFrame({"a": ["x"], "b": ["y"]})
        assert get_numeric_columns(df) == []


# ── Tests for get_top_n_rows ──────────────────────────────────────


class TestGetTopNRows:
    """Tests for the get_top_n_rows function."""

    def test_returns_correct_count(self, sample_df: pd.DataFrame) -> None:
        """Should return exactly n rows."""
        result = get_top_n_rows(sample_df, 3)
        assert len(result) == 3

    def test_n_greater_than_length(self, sample_df: pd.DataFrame) -> None:
        """Should return all rows when n exceeds DataFrame length."""
        result = get_top_n_rows(sample_df, 100)
        assert len(result) == len(sample_df)

    def test_invalid_n_raises(self, sample_df: pd.DataFrame) -> None:
        """Should raise ValueError for n <= 0."""
        with pytest.raises(ValueError, match="positive integer"):
            get_top_n_rows(sample_df, 0)

    def test_large_dataframe(self, large_df: pd.DataFrame) -> None:
        """Should work correctly with larger DataFrames."""
        result = get_top_n_rows(large_df, 50)
        assert len(result) == 50
