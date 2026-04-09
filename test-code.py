from flask import Flask, request
import sqlite3

app = Flask(__name__)

# ❌ Insecure: hardcoded secret key
app.secret_key = "supersecretkey"


# ❌ Insecure: SQL Injection vulnerability
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ❌ Vulnerable query (no parameterization)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful"
    return "Invalid credentials"


# ❌ Insecure: Command Injection
@app.route("/ping", methods=["GET"])
def ping():
    import os
    host = request.args.get("host")

    # ❌ Direct command execution
    result = os.popen(f"ping -c 1 {host}").read()
    return result


# ❌ Insecure: Debug mode enabled
if __name__ == "__main__":
    app.run(debug=True)
