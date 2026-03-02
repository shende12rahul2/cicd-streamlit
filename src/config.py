"""Centralized application configuration.

All constants, defaults, and environment-driven settings live here.
Import from this module instead of scattering magic values across files.
"""

from __future__ import annotations

import os

# ── File upload limits ──────────────────────────────────────────────
ALLOWED_EXTENSIONS: frozenset = frozenset({".csv"})
MAX_FILE_SIZE_MB: int = int(os.getenv("CSV_ANALYZER_MAX_FILE_MB", "50"))

# ── Data preview defaults ───────────────────────────────────────────
DEFAULT_PREVIEW_ROWS: int = 10
MAX_PREVIEW_ROWS: int = 10_000

# ── Search / filter ─────────────────────────────────────────────────
MAX_SEARCH_TERM_LENGTH: int = 200

# ── Application metadata ───────────────────────────────────────────
APP_TITLE: str = "CSV Data Analyzer"
APP_ICON: str = "📊"
APP_VERSION: str = "1.1.0"
