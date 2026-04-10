import os
import pickle
import sqlite3

from flask import Flask, request

app = Flask(__name__)


# 🚨 SQL Injection vulnerability
@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Dangerous query (no sanitization)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    return str(cursor.fetchall())


# 🚨 Command Injection vulnerability
@app.route("/ping")
def ping():
    host = request.args.get("host")

    # Dangerous OS command execution
    result = os.popen(f"ping -c 1 {host}").read()
    return result


# 🚨 Hardcoded secret
SECRET_KEY = "super-secret-password"

# 🚨 Insecure deserialization


@app.route("/load", methods=["POST"])
def load_data():
    data = request.data
    obj = pickle.loads(data)  # ⚠️ RCE risk
    return str(obj)


if __name__ == "__main__":
    app.run(debug=True)
