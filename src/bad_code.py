import hashlib
import random
import sqlite3
import tempfile

from flask import Flask, request

app = Flask(__name__)


# CRITICAL: Remote Code Execution (Code Injection)
@app.route("/exec")
def execute_code():
    code = request.args.get("code")
    # Rule: py/code-injection
    exec(code)
    return "Executed"


# HIGH: SQL Injection
@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Rule: py/sql-injection
    cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    return str(cursor.fetchall())


# MEDIUM: Insecure Randomness and Hardcoded Credentials
@app.route("/login")
def login():
    # Rule: py/hardcoded-credentials
    secret_password = "SuperSecretAdminPassword123!"  # noqa: F841
    # Rule: py/insecure-randomness
    token = str(random.random())
    return token


# LOW: Insecure Temporary File and Weak Cryptography
@app.route("/hash")
def hash_data():
    data = request.args.get("data", "default")
    # Rule: py/weak-crypto
    md5_hash = hashlib.md5(data.encode()).hexdigest()

    # Rule: py/insecure-temporary-file
    tmp_file = tempfile.mktemp()  # noqa: F841
    return md5_hash


if __name__ == "__main__":
    app.run()
