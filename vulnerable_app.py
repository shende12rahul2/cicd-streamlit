"""
vulnerable_app.py
---------------------------------------------------------
DEMO FILE — intentional critical security vulnerabilities
for CodeQL detection testing.
DO NOT deploy or use in any real environment.
---------------------------------------------------------

CodeQL rules that WILL fire on this file:
  py/sql-injection               (critical)
  py/reflected-xss               (critical)
  py/code-injection              (critical)
  py/path-traversal              (critical)
  py/hardcoded-credentials       (critical)
  py/command-injection           (critical)
  py/xml-injection               (critical / XXE)
"""

import os
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ─── VULNERABILITY 1: Hardcoded credentials ──────────────────────────────────
# CodeQL: py/hardcoded-credentials
# Credentials embedded in source — visible in version control forever.
DB_PASSWORD  = "prod_password_123"          # ← hardcoded credential
SECRET_KEY   = "flask_secret_never_rotate"  # ← hardcoded secret
API_KEY      = "sk-abcdef1234567890abcdef"  # ← hardcoded API key

app.secret_key = SECRET_KEY


# ─── VULNERABILITY 2: SQL Injection ──────────────────────────────────────────
# CodeQL: py/sql-injection
# User-supplied input is formatted directly into a SQL string.
# Attacker payload: username = ' OR '1'='1' --
@app.route('/user')
def get_user():
    username = request.args.get('username', '')
    conn     = sqlite3.connect('users.db')
    cursor   = conn.cursor()

    # VULNERABLE — f-string interpolation into SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()
    return str(rows)


# ─── VULNERABILITY 3: Reflected Cross-Site Scripting (XSS) ───────────────────
# CodeQL: py/reflected-xss
# render_template_string with user input and the | safe filter bypasses
# Jinja2 auto-escaping, reflecting raw HTML/JS back to the browser.
# Attacker payload: q = <script>alert(document.cookie)</script>
@app.route('/search')
def search():
    search_term = request.args.get('q', '')

    # VULNERABLE — user input marked |safe disables all escaping
    template = f"<h1>Results for: { search_term | safe }</h1>"
    return render_template_string(template)


# ─── VULNERABILITY 4: Code Injection via exec() / eval() ─────────────────────
# CodeQL: py/code-injection
# Arbitrary Python sent by the client is executed on the server.
@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form.get('expression', '')

    # VULNERABLE — eval() on untrusted input allows full server-side execution
    result = eval(expression)
    return str(result)


# ─── VULNERABILITY 5: Path Traversal ─────────────────────────────────────────
# CodeQL: py/path-traversal
# A user-controlled filename is used in open() without canonicalisation.
# Attacker payload: filename = ../../../../etc/passwd
@app.route('/file')
def read_file():
    filename = request.args.get('filename', '')

    # VULNERABLE — no os.path.realpath() or containment check
    file_path = '/var/app/uploads/' + filename

    with open(file_path, 'r') as f:
        return f.read()


# ─── VULNERABILITY 6: Command Injection ──────────────────────────────────────
# CodeQL: py/command-injection
# User input is passed to the shell without sanitisation.
# Attacker payload: host = 127.0.0.1; cat /etc/shadow
@app.route('/ping')
def ping():
    host = request.args.get('host', '')

    # VULNERABLE — shell=True + user-controlled string = arbitrary OS commands
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


# ─── VULNERABILITY 7: XML External Entity (XXE) Injection ────────────────────
# CodeQL: py/xml-injection  (also caught by semgrep XXE rules)
# The default xml.etree.ElementTree parser resolves external entities,
# allowing an attacker to read local files or trigger SSRF.
# Attacker payload: XML with <!ENTITY xxe SYSTEM "file:///etc/passwd">
@app.route('/upload-xml', methods=['POST'])
def upload_xml():
    xml_data = request.data

    # VULNERABLE — ET.fromstring does not disable external entity processing
    root = ET.fromstring(xml_data)
    return root.tag


if __name__ == '__main__':
    # debug=True also leaks full stack traces to the browser — another finding
    app.run(debug=True, host='0.0.0.0', port=5000)
