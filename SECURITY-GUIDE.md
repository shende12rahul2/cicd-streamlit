# 🔐 Security Alert Guide for Developers

This document explains where to find and how to fix the three types of security alerts
enabled on this repository via **GitHub Advanced Security (GHAS)**:
CodeQL code scanning, Dependabot vulnerability alerts, and Secret scanning.

---

## Table of Contents

1. [CodeQL — Code Vulnerabilities](#1-codeql--code-vulnerabilities)
2. [Dependabot — Vulnerable Dependencies](#2-dependabot--vulnerable-dependencies)
3. [Secret Scanning — Exposed Credentials](#3-secret-scanning--exposed-credentials)
4. [How the PR Gate Works](#4-how-the-pr-gate-works)
5. [Severity Reference](#5-severity-reference)
6. [Fix Checklist](#6-fix-checklist)

---

## 1. CodeQL — Code Vulnerabilities

CodeQL scans your code for security vulnerabilities such as SQL injection,
command injection, path traversal, XSS, and hardcoded credentials.

### Where to find alerts

**In a Pull Request:**

When you open a PR to `dev` or `main`, the `Security Gate / Block Critical` job
posts a comment directly on the PR listing all **Critical**, **High**, **Medium**, and **Low** findings.

```
PR → bottom of page → CodeQL Security Findings comment
```

The comment shows:

| Column | What it means |
|---|---|
| Severity | 🚨 CRITICAL, ⚠️ HIGH, 🔵 MEDIUM, or ⚪ LOW |
| Rule | The CodeQL rule ID e.g. `js/sql-injection` |
| File | The file and line number with the issue |
| Description | Short explanation of the vulnerability |
| Link | Direct link to the full alert in the Security tab |

**In the Security tab (all branches):**

```
Repository → Security → Code scanning alerts
```

Filter by:
- **Branch** — select `main` or `dev` to see what is live
- **Severity** — filter by Critical / High / Medium
- **State** — Open alerts are unresolved

Click any alert to see:
- The exact line of code flagged
- A full explanation of why it is dangerous
- A **Show paths** link that traces how user input flows to the vulnerable sink

### How to fix

1. Open the alert link from the PR comment or the Security tab
2. Read the **Show paths** section — it shows the full data flow from source to sink
3. Apply the fix (see common patterns below)
4. Push your fix — CodeQL rescans automatically and closes the alert if the issue is gone

**Common fixes:**

| Rule | Vulnerable pattern | Safe pattern |
|---|---|---|
| `js/sql-injection` | `"SELECT * WHERE id = " + input` | Parameterised query: `db.query("SELECT * WHERE id = ?", [input])` |
| `py/sql-injection` | `f"SELECT * WHERE id = '{input}'"` | `cursor.execute("SELECT * WHERE id = ?", (input,))` |
| `js/command-injection` | `` exec(`ping ${host}`) `` | Use `execFile` with args array, never `shell: true` |
| `py/command-injection` | `subprocess.run(f"ping {host}", shell=True)` | `subprocess.run(["ping", "-c", "1", host])` |
| `js/path-traversal` | `fs.readFile('/uploads/' + filename)` | `path.resolve` + check result starts with allowed dir |
| `js/code-injection` | `eval(userInput)` | Remove `eval` — use a safe expression parser |
| `js/reflected-xss` | `res.send('<h1>' + input + '</h1>')` | Escape output: use a template engine with auto-escaping |
| `js/hardcoded-credentials` | `password: 'abc123'` | Move to environment variable or secrets manager |

---

## 2. Dependabot — Vulnerable Dependencies

Dependabot watches your `package.json`, `requirements.txt`, `Dockerfile`,
and GitHub Actions for dependencies with known CVEs.

> **Note:** Dependabot is configured to send **alerts only** — it does NOT
> open automatic pull requests. You must apply fixes manually.

### Where to find alerts

```
Repository → Security → Dependabot alerts
```

Each alert shows:

| Field | What it means |
|---|---|
| Package | The dependency with the vulnerability e.g. `lodash` |
| Severity | Critical / High / Medium / Low |
| CVE | The CVE identifier e.g. `CVE-2021-23337` |
| Vulnerable versions | Which versions are affected |
| Patched version | The version that fixes the issue |
| Manifest | Which file pulls this dependency e.g. `package.json` |

### How to fix

**JavaScript / npm:**
```bash
# Check what is vulnerable
npm audit

# Update a specific package
npm install lodash@4.17.21

# Update all within semver range
npm update

# Force fix (use with caution — may break things)
npm audit fix
```

**Python / pip:**
```bash
# Check what is vulnerable
pip-audit   # install with: pip install pip-audit

# Update a specific package
pip install --upgrade requests

# Update requirements.txt
pip install -r requirements.txt --upgrade
```

**GitHub Actions dependencies:**

If a Dependabot alert points to a workflow file, update the action version
in the relevant `.github/workflows/*.yml` file and verify the new SHA.

### Dismissing an alert

Only dismiss if the vulnerability does not affect your usage. When dismissing,
always select a reason:

- **Tolerable risk** — the vulnerable code path is not reachable in your app
- **No bandwidth to fix** — acceptable only for low/medium, never for critical/high

---

## 3. Secret Scanning — Exposed Credentials

Secret scanning detects API keys, tokens, passwords, and private keys that have
been committed to the repository.

> **Push protection is enabled** — GitHub will block a `git push` if it
> detects a secret in the new commit before it reaches the remote.

### Where to find alerts

```
Repository → Security → Secret scanning alerts
```

Each alert shows:

| Field | What it means |
|---|---|
| Secret type | What kind of secret e.g. `GitHub token`, `AWS access key` |
| Location | The file and commit where it was found |
| State | Active (unresolved) or Resolved |

### What to do immediately when you see an alert

> ⚠️ Assume the secret is already compromised — treat it as leaked even if the
> repo is private.

**Step 1 — Rotate the secret immediately**

| Secret type | Where to rotate |
|---|---|
| GitHub personal access token | GitHub → Settings → Developer settings → Tokens |
| AWS access key | AWS Console → IAM → Users → Security credentials |
| Google API key | Google Cloud Console → APIs & Services → Credentials |
| Stripe / payment key | Payment provider dashboard → API keys |
| Database password | Your database admin panel or cloud console |
| JWT secret | Generate a new secret and redeploy |

**Step 2 — Remove it from the code**

```bash
# Remove the secret from the file
# Then commit the clean version
git add .
git commit -m "fix: remove hardcoded secret"
git push
```

> **The secret is still in git history** even after you delete it from the file.
> If the repo is public or the secret is high risk, you must also purge history:

```bash
# Purge from history using git filter-repo (preferred over BFG)
pip install git-filter-repo
git filter-repo --path-glob '**' --replace-text <(echo 'OLD_SECRET==>REMOVED')
git push --force
```

**Step 3 — Move to a safe location**

Never put secrets in source code. Use one of:

```bash
# Option 1: Environment variable (local dev)
export DATABASE_PASSWORD="your-password"

# Option 2: .env file (never commit this file)
echo ".env" >> .gitignore

# Option 3: GitHub Actions secret (for CI/CD)
# Repository → Settings → Secrets and variables → Actions → New secret
# Then reference in workflow:
# password: ${{ secrets.DATABASE_PASSWORD }}

# Option 4: Cloud secrets manager
# AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, HashiCorp Vault
```

**Step 4 — Resolve the alert**

Once rotated and removed, go to the alert and mark it as **Resolved → Revoked**.

---

## 4. How the PR Gate Works

```
Open PR to dev or main
        ↓
CodeQL Analyze runs (scans JS + Python)
        ↓
Security Gate job runs after scan completes
        ↓
  ┌─────────────────────────────────────┐
  │ Critical findings found?            │
  │                                     │
  │  YES → ❌ Status check FAILS        │
  │         Merge button is DISABLED    │
  │         PR comment lists findings  │
  │                                     │
  │  NO  → ✅ Status check PASSES       │
  │         Merge button is ENABLED     │
  └─────────────────────────────────────┘
```

**Required status checks (must pass before merge):**

- `CodeQL Analyze (javascript-typescript)`
- `CodeQL Analyze (python)`
- `Security Gate / Block Critical`

If any of these are red, the PR cannot be merged regardless of approvals.

**High/Medium/Low severity findings** — do not block the merge. They appear alongside critical alerts in the PR comment table so reviewers are aware of them, but they can be safely resolved later.

### 4.1 Troubleshooting: "Merging is blocked" Errors

Sometimes GitHub's internal expectations fall out of sync with our configurations, resulting in errors like:
> **"Code scanning is still expecting 1 result from CodeQL"**

![Placeholder for PR Merge Blocked Error Image]()
*(Developer Note: Insert screenshot of the blocked PR merge button here)*

If your CodeQL workflows (`javascript` / `python`) show as green and successful, but the PR is still blocked by the above message, here is how you fix it:

**Scenario A: Typo in Required Status Checks**
If `CodeQL` was manually entered into your Branch Protection settings, GitHub awaits an Action expressly named `CodeQL` (which doesn't exist).
1. Go to **Settings** → **Branches**
2. Edit your branch protection rule (e.g., `dev` or `main`)
3. Remove any entries that just say `CodeQL`
4. Ensure we only require specific jobs (e.g., `CodeQL Analyze (javascript)`)

![Placeholder for GitHub Branch Protection Settings Image]()
*(Developer Note: Insert screenshot of the branch protection configuration here)*

**Scenario B: Default Setup vs. Advanced Setup Conflict**
If automatic "Default Setup" is on, it conflicts with our custom `codeql.yml` workflows.
1. Go to **Settings** → **Code security and analysis** → **Code scanning**
2. If "Default setup" is enabled, disable it.

![Placeholder for Code Scanning Settings Disable Default Setup Image]()
*(Developer Note: Insert screenshot of disabling default Code Scanning setup here)*

**Scenario C: Broken Baseline Expectation**
If the base branch (`dev` or `main`) has a different CodeQL configuration than the PR branch, expectations misalign.
* **Fix / Bypass:** Push an empty commit to force a fresh CodeQL run and re-synchronize exactly what should be expected:
```bash
git commit --allow-empty -m "trigger codeql"
git push origin <your-branch-name>
```

---

## 5. Severity Reference

| Severity | CodeQL blocks merge? | Dependabot action required | Secret scanning action required |
|---|---|---|---|
| 🚨 **Critical** | ✅ Yes — merge blocked | Fix immediately | Rotate + remove immediately |
| ⚠️ **High** | ❌ No — warning only | Fix within current sprint | Rotate + remove immediately |
| 🔵 **Medium** | ❌ No — Security tab only | Fix within next sprint | Assess and plan fix |
| ⚪ **Low** | ❌ No — Security tab only | Fix when convenient | Assess and plan fix |

---

## 6. Fix Checklist

Use this checklist when resolving a security alert before your PR can merge.

### CodeQL alert
- [ ] Opened the alert and read the **Show paths** data flow
- [ ] Identified the source (user input) and the sink (dangerous function)
- [ ] Applied a fix — parameterised query / safe API / input validation
- [ ] Pushed the fix and confirmed the CodeQL rescan closed the alert
- [ ] PR comment no longer shows the finding

### Dependabot alert
- [ ] Read the CVE description and confirmed it affects your usage
- [ ] Updated the dependency to the patched version
- [ ] Ran the test suite to confirm nothing broke
- [ ] Verified the Dependabot alert is now closed


### Secret scanning alert
- [ ] Rotated the exposed secret in the provider dashboard
- [ ] Removed the secret from the source file
- [ ] Added the secret to `.gitignore` / environment variables / GitHub Secrets
- [ ] Checked git history — purged if necessary
- [ ] Marked the alert as **Resolved → Revoked**

---

> For questions, contact the security team or open a GitHub Issue with the
> label `security`.
