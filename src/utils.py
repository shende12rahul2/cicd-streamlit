"""Utility functions for CSV data analysis.

This module contains all business logic for data processing,
statistics computation, and data filtering — separated from UI.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(file: Any) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame.

    Args:
        file: A file-like object (e.g., Streamlit UploadedFile).

    Returns:
        A pandas DataFrame with the parsed CSV data.

    Raises:
        ValueError: If the file is empty or cannot be parsed.
    """
    try:
        df = pd.read_csv(file)
    except pd.errors.EmptyDataError as exc:
        logger.error("CSV load failed: file is empty")
        raise ValueError("The uploaded file is empty.") from exc
    except pd.errors.ParserError as exc:
        logger.error("CSV load failed: parse error — %s", exc)
        raise ValueError("Unable to parse the file. Ensure it is a valid CSV.") from exc

    if df.empty:
        logger.warning("CSV loaded but contains no data rows")
        raise ValueError("The CSV file contains no data rows.")

    logger.info("CSV loaded: %d rows × %d columns", len(df), df.shape[1])
    return df


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics for all numeric columns.

    Args:
        df: Input DataFrame.

    Returns:
        A DataFrame with count, mean, std, min, 25%, 50%, 75%, max
        for each numeric column.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame({"info": ["No numeric columns found"]})
    return numeric_df.describe().round(2)


def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """Return metadata about each column in the DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        A DataFrame with column name, dtype, non-null count,
        null count, and unique value count.
    """
    info = pd.DataFrame(
        {
            "Column": df.columns,
            "Data Type": [str(dtype) for dtype in df.dtypes],
            "Non-Null Count": [df[col].notna().sum() for col in df.columns],
            "Null Count": [df[col].isna().sum() for col in df.columns],
            "Unique Values": [df[col].nunique() for col in df.columns],
        }
    )
    return info


def filter_dataframe(
    df: pd.DataFrame,
    column: str,
    search_term: str,
) -> pd.DataFrame:
    """Filter a DataFrame by searching for a term in a specific column.

    The search is case-insensitive and uses substring matching.

    Args:
        df: Input DataFrame.
        column: Name of the column to search in.
        search_term: The substring to search for.

    Returns:
        A filtered DataFrame containing only matching rows.

    Raises:
        KeyError: If the column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in the DataFrame.")

    col_data = df[column].astype(str)
    mask = col_data.str.contains(search_term, case=False, na=False)
    result: pd.DataFrame = df[mask]
    logger.info(
        "Filter on '%s' for '%s': %d/%d rows matched",
        column,
        search_term,
        len(result),
        len(df),
    )
    return result


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """Return a list of numeric column names.

    Args:
        df: Input DataFrame.

    Returns:
        List of column names that have numeric dtypes.
    """
    result: list[str] = df.select_dtypes(include=[np.number]).columns.tolist()
    return result


def get_top_n_rows(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N rows of a DataFrame.

    Args:
        df: Input DataFrame.
        n: Number of rows to return (default: 10).

    Returns:
        A DataFrame with at most n rows.

    Raises:
        ValueError: If n is not a positive integer.
    """
    if n <= 0:
        raise ValueError("Number of rows must be a positive integer.")
    return df.head(n)
