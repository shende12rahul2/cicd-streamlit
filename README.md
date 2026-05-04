# 📊 CSV Data Analyzer — Streamlit App

[![CI](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml)
[![CodeQL](https://github.com/<OWNER>/<REPO>/actions/workflows/codeql.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/<OWNER>/<REPO>/badge)](https://securityscorecards.dev/viewer/?uri=github.com/<OWNER>/<REPO>)

> **Note:** Replace `<OWNER>/<REPO>` above with your GitHub org/repo name.

A production-ready Streamlit application for CSV data exploration and analysis. Built with a modular architecture, enforced code quality, and **GitHub Advanced Security** integration.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **CSV Upload** | Upload any `.csv` file (up to 50 MB) |
| **Data Preview** | Configurable row count preview |
| **Summary Statistics** | Auto-generated stats for numeric columns |
| **Column Info** | Data types, null counts, unique values |
| **Data Filtering** | Case-insensitive substring search on any column |
| **Input Validation** | File type, size, and user input validation |

---

## 📁 Project Structure

```
streamlit-app/
├── app.py                          # Streamlit UI entry point
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Tool config (Black, Ruff, mypy, coverage)
├── Makefile                        # Dev workflow automation
├── .pre-commit-config.yaml         # 12 pre-commit hooks
├── .gitignore
├── .editorconfig
├── .secrets.baseline               # detect-secrets baseline
├── .gitlab-ci.yml                  # GitLab CI (optional)
├── .github/
│   ├── dependabot.yml              # Automated dependency updates
│   └── workflows/
│       ├── ci.yml                  # Lint, Test, Security, Type Check
│       ├── codeql.yml              # CodeQL semantic analysis (GHAS)
│       ├── dependency-review.yml   # Block vulnerable deps on PRs (GHAS)
│       └── scorecard.yml           # OpenSSF supply-chain assessment
├── src/
│   ├── __init__.py
│   ├── config.py                   # Centralized constants
│   ├── utils.py                    # Business logic + structured logging
│   └── validation.py               # Input validation helpers
└── tests/
    ├── __init__.py
    ├── conftest.py                 # Shared fixtures
    ├── test_utils.py               # Utility tests
    └── test_validation.py          # Validation tests
```

---

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.8+** (3.11 recommended)
- **pip** · **Git** · **make** (optional)

### Quick Start

```bash
cd streamlit-app
make install        # Creates venv, installs deps, sets up pre-commit
source .venv/bin/activate
make run            # Starts Streamlit at http://localhost:8501
```

### Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
git init
pre-commit install
detect-secrets scan > .secrets.baseline
```

---

## ▶️ Running the Application

```bash
make run
# or: streamlit run app.py
```

---

## 🧪 Running Tests

```bash
make test           # pytest + coverage (fails if < 80%)
# or: pytest -v --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## 🔧 Makefile Targets

| Target | Description |
|--------|-------------|
| `make install` | Create venv, install deps, setup pre-commit |
| `make format` | Auto-format with Black + isort |
| `make lint` | Ruff, Black check, isort check |
| `make test` | pytest with 80% coverage gate |
| `make security` | Bandit + detect-secrets scan |
| `make typecheck` | mypy type checking |
| `make ci` | Run **full CI pipeline locally** |
| `make run` | Start Streamlit app |
| `make clean` | Remove caches and venv |

---

## 🔐 GitHub Advanced Security (GHAS)

This project uses all major GHAS features for enterprise-grade security.

### Workflows Overview

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `ci.yml` | PR + push to main | Lint, test, Bandit SARIF, detect-secrets, mypy |
| **CodeQL** | `codeql.yml` | PR + push + weekly | Semantic code analysis (security-extended queries) |
| **Dependency Review** | `dependency-review.yml` | PR only | Block vulnerable/licensed deps |
| **Scorecard** | `scorecard.yml` | Push to main + weekly | OpenSSF supply-chain assessment |

### Security Best Practices Applied

| Practice | Implementation |
|----------|---------------|
| **Pinned action SHAs** | All `uses:` reference full commit SHAs, not tags |
| **Least-privilege permissions** | Each job declares only the permissions it needs |
| **Concurrency control** | Stale CI runs are auto-cancelled on new pushes |
| **SARIF uploads** | Bandit + CodeQL + Scorecard results → Code Scanning tab |
| **Dependency Review** | PRs blocked if they add high/critical CVE dependencies |
| **Dependabot** | Auto-PRs for pip + GitHub Actions version updates |
| **Secret scanning** | detect-secrets in CI + GitHub native secret scanning |
| **Coverage gating** | Tests must maintain ≥80% code coverage |

### Where to See Results

| Feature | Location in GitHub |
|---------|--------------------|
| CI status | Pull Request → Checks tab |
| Code Scanning alerts | Security tab → Code scanning |
| Dependency alerts | Security tab → Dependabot |
| Scorecard results | Security tab → Code scanning (category: scorecard) |
| Coverage report | CI artifacts → `coverage.xml` |

---

## 🔧 Pre-commit Hooks (12 hooks)

| Hook | Purpose |
|------|---------|
| trailing-whitespace | Trim trailing whitespace |
| end-of-file-fixer | Ensure files end with newline |
| check-yaml / check-toml | Validate config files |
| check-added-large-files | Block files > 500 KB |
| check-merge-conflict | Detect merge conflicts |
| **Black** | Code formatting |
| **isort** | Import sorting |
| **Ruff** | Fast linter + auto-fix |
| **Bandit** | Security scan |
| **detect-secrets** | Prevent secret leaks |
| **mypy** | Static type checking |

```bash
pre-commit run --all-files    # Run all hooks
```

---

## 📝 Code Quality Standards

- ✅ Type hints on all functions
- ✅ Docstrings on all public functions
- ✅ No hardcoded credentials (enforced by detect-secrets + Bandit + GHAS)
- ✅ Input validation on all user inputs
- ✅ Separation of concerns — UI / logic / config
- ✅ Structured logging in business logic
- ✅ 80% test coverage minimum (enforced in CI)
- ✅ All actions pinned to SHA (supply-chain security)

---

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run `make ci` to verify locally
4. Push and open a **Pull Request**
5. CI + CodeQL + Dependency Review run automatically
6. Get code review and merge

---

## 📜 License
This security check of code
MIT
Apache 2.0
123
