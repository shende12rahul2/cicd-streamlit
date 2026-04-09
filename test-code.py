from flask import Flask, request
import sqlite3
import subprocess
import pickle
import requests
import os

app = Flask(__name__)

# ❌ Hardcoded secret (HIGH)
app.config["SECRET_KEY"] = "hardcoded-production-secret"


# ❌ SQL Injection (HIGH)
@app.route("/user")
def get_user():
    user_id = request.args.get("id")

    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)

    return str(cursor.fetchall())


# ❌ Remote Command Execution (CRITICAL)
@app.route("/exec")
def exec_cmd():
    cmd = request.args.get("cmd")

    result = subprocess.check_output(cmd, shell=True)
    return result.decode()


# ❌ Arbitrary File Read (HIGH)
@app.route("/file")
def read_file():
    path = request.args.get("path")

    with open(path, "r") as f:
        return f.read()


# ❌ Insecure Deserialization (CRITICAL)
@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data

    obj = pickle.loads(data)  # ⚠️ RCE possible
    return str(obj)


# ❌ SSRF (HIGH)
@app.route("/fetch")
def fetch():
    url = request.args.get("url")

    response = requests.get(url)
    return response.text


# ❌ Unsafe eval (CRITICAL)
@app.route("/eval")
def run_eval():
    code = request.args.get("code")

    return str(eval(code))  # ⚠️ Arbitrary code execution


# ❌ Unsafe OS command (CRITICAL - alternative pattern)
@app.route("/os")
def os_cmd():
    cmd = request.args.get("cmd")

    return os.system(cmd)


if __name__ == "__main__":
    app.run()
