import hashlib
import sqlite3
import ssl
import subprocess
import tempfile

from flask import Flask, request

app = Flask(__name__)


# CRITICAL: Remote Code Execution via Subprocess
@app.route("/execute")
def execute_system_command():
    user_input = request.args.get("cmd")
    # Rule: py/command-line-injection
    subprocess.run(user_input, shell=True)  # noqa: S602
    return "Executed"


# HIGH: SQL Injection
@app.route("/search")
def search_database():
    query = request.args.get("q")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Rule: py/sql-injection
    cursor.execute(f"SELECT * FROM items WHERE name = '{query}'")
    return str(cursor.fetchall())


# MEDIUM: Hardcoded Secrets
@app.route("/admin/login")
def admin_login():
    # Rule: py/hardcoded-credentials
    AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"  # noqa: F841
    return "Attempting login"


# LOW: Weak Hashing Algorithm
@app.route("/password_reset")
def reset_password():
    new_password = request.args.get("pwd", "default123")
    # Rule: py/weak-crypto
    hashed_password = hashlib.md5(new_password.encode()).hexdigest()
    return hashed_password


# LOW: Insecure Temporary File Creation
def create_temp_report():
    # Rule: py/insecure-temporary-file
    report_file = tempfile.mktemp()  # noqa: F841
    return "Report created"


# LOW: Insecure SSL Context
def fetch_external_data():
    # Rule: py/insecure-certificate-validation
    secure_context = ssl._create_unverified_context()
    return str(secure_context)


if __name__ == "__main__":
    app.run(debug=True)
