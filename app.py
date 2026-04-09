"""CSV Data Analyzer — Streamlit Application.

A production-ready CSV upload & analysis tool with a clean,
modular architecture. UI logic lives here; business logic
lives in the ``src`` package.
"""

from __future__ import annotations

import sys

import pandas as pd
import streamlit as st

from src.config import APP_ICON, APP_TITLE, APP_VERSION
from src.utils import (
    filter_dataframe,
    get_column_info,
    get_numeric_columns,
    get_summary_statistics,
    get_top_n_rows,
    load_csv,
)
from src.validation import (
    validate_file_extension,
    validate_file_size,
    validate_row_count_input,
    validate_search_term,
)

# ── Page configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 0.75rem;
        color: white;
        text-align: center;
    }
    .metric-card h3 { margin: 0; font-size: 0.85rem; opacity: 0.9; }
    .metric-card p  { margin: 0; font-size: 1.8rem; font-weight: 700; }
    .success-box {
        padding: 0.75rem 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.4rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _render_header() -> None:
    """Render the application header."""
    st.markdown(
        f'<p class="main-header">{APP_ICON} {APP_TITLE}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">'
        "Upload a CSV file to explore summary statistics, filter data, "
        "and gain quick insights."
        "</p>",
        unsafe_allow_html=True,
    )


def _render_metrics(df: pd.DataFrame) -> None:
    """Display key metrics as styled cards."""
    num_cols = get_numeric_columns(df)
    cols = st.columns(4)
    metrics = [
        ("Rows", f"{len(df):,}"),
        ("Columns", str(df.shape[1])),
        ("Numeric Cols", str(len(num_cols))),
        ("Missing Cells", f"{int(df.isna().sum().sum()):,}"),
    ]
    for col, (label, value) in zip(cols, metrics):
        col.markdown(
            f'<div class="metric-card"><h3>{label}</h3><p>{value}</p></div>',
            unsafe_allow_html=True,
        )


def _render_sidebar() -> st.runtime.uploaded_file_manager.UploadedFile | None:
    """Render the sidebar with file uploader and instructions."""
    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")
        uploaded_file = st.file_uploader(
            "Upload your CSV file",
            type=["csv"],
            help="Maximum file size: 50 MB",
        )
        st.markdown("---")
        st.markdown(
            "**How to use:**\n"
            "1. Upload a `.csv` file\n"
            "2. Explore the auto-generated summary\n"
            "3. Use the **Filter** tab to search\n"
            "4. Adjust the preview row count"
        )
        st.markdown("---")
        st.caption(f"v{APP_VERSION} · Streamlit · Python {python_ver}")
    return uploaded_file


def _render_analysis_tabs(df: pd.DataFrame) -> None:
    """Render the main analysis area with tabs."""
    tab_preview, tab_stats, tab_info, tab_filter = st.tabs(
        ["📋 Data Preview", "📈 Statistics", "ℹ️ Column Info", "🔍 Filter"]
    )

    # ── Data Preview ────────────────────────────────────────────────
    with tab_preview:
        st.subheader("Data Preview")
        row_input = st.text_input(
            "Number of rows to display",
            value="10",
            key="row_count",
        )
        is_valid, n_rows, msg = validate_row_count_input(row_input)
        if is_valid:
            preview = get_top_n_rows(df, n_rows)
            st.dataframe(preview, use_container_width=True)
            st.caption(f"Showing {len(preview)} of {len(df):,} rows")
        else:
            st.warning(msg)

    # ── Summary Statistics ──────────────────────────────────────────
    with tab_stats:
        st.subheader("Summary Statistics")
        stats = get_summary_statistics(df)
        st.dataframe(stats, use_container_width=True)

    # ── Column Info ─────────────────────────────────────────────────
    with tab_info:
        st.subheader("Column Information")
        col_info = get_column_info(df)
        st.dataframe(col_info, use_container_width=True)

    # ── Filter Data ─────────────────────────────────────────────────
    with tab_filter:
        st.subheader("Filter Data")
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_column = st.selectbox(
                "Select column to search",
                options=df.columns.tolist(),
                key="filter_col",
            )
        with col2:
            search_term = st.text_input(
                "Enter search term",
                key="search_term",
                placeholder="Type to search…",
            )

        if st.button("🔍 Apply Filter", type="primary", key="apply_filter"):
            term_valid, term_msg = validate_search_term(search_term)
            if not term_valid:
                st.warning(term_msg)
            else:
                filtered = filter_dataframe(df, selected_column, search_term)
                if filtered.empty:
                    st.info("No rows matched your search.")
                else:
                    st.markdown(
                        f'<div class="success-box">'
                        f"Found <strong>{len(filtered):,}</strong> matching rows."
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    st.dataframe(filtered, use_container_width=True)


# ── Main ────────────────────────────────────────────────────────────
def main() -> None:
    """Application entry point."""
    _render_header()
    uploaded_file = _render_sidebar()

    if uploaded_file is None:
        st.info("👈 Upload a CSV file from the sidebar to get started.")
        return

    # Validate file
    ext_ok, ext_msg = validate_file_extension(uploaded_file.name)
    if not ext_ok:
        st.error(ext_msg)
        return

    size_ok, size_msg = validate_file_size(uploaded_file.size)
    if not size_ok:
        st.error(size_msg)
        return

    # Load & analyse
    try:
        df = load_csv(uploaded_file)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.markdown(
        f'<div class="success-box">✅ <strong>{uploaded_file.name}</strong> '
        f"loaded successfully — {size_msg}</div>",
        unsafe_allow_html=True,
    )

    _render_metrics(df)
    st.markdown("---")
    _render_analysis_tabs(df)





if __name__ == "__main__":
    main()



