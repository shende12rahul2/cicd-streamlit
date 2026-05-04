import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

# ✅ Use environment variable for secrets
SECRET_KEY = os.environ.get("SECRET_KEY", "default-safe-key")


# ✅ SQL Injection FIX (parameterized query)
@app.route("/user")
def get_user():
    user_id = request.args.get("id")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    return jsonify(cursor.fetchall())


# ✅ Command Injection FIX (input validation)
@app.route("/ping")
def ping():
    host = request.args.get("host")

    if not host or not host.replace(".", "").isalnum():
        return "Invalid host", 400

    result = os.popen(f"ping -c 1 {host}").read()
    return result


# ✅ Remove insecure deserialization
@app.route("/load", methods=["POST"])
def load_data():
    return "Deserialization disabled for security", 403


if __name__ == "__main__":
    app.run(debug=False)
