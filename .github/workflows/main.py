from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os
import pickle
import yaml
import requests
import base64

app = Flask(__name__)

# ❌ HARD CODED SECRETS (HIGH)
app.config["SECRET_KEY"] = "super-secret-prod-key"
DB_PASSWORD = "root123"
API_KEY = "12345-SECRET-KEY"


# ❌ INSECURE LOGGING (INFO LEAK)
def log(message):
    with open("app.log", "a") as f:
        f.write(message + "\n")


# ❌ SQL INJECTION (HIGH)
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    return str(cursor.fetchall())


# ❌ SECOND SQL INJECTION VARIANT
@app.route("/product")
def product():
    pid = request.args.get("id")
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id=" + pid)
    return str(cursor.fetchall())


# ❌ COMMAND INJECTION (CRITICAL)
@app.route("/ping")
def ping():
    host = request.args.get("host")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


# ❌ OS COMMAND EXECUTION (CRITICAL)
@app.route("/exec")
def exec_cmd():
    cmd = request.args.get("cmd")
    return str(os.system(cmd))


# ❌ EVAL INJECTION (CRITICAL)
@app.route("/eval")
def run_eval():
    code = request.args.get("code")
    return str(eval(code))


# ❌ UNSAFE DESERIALIZATION (CRITICAL)
@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data
    obj = pickle.loads(data)
    return str(obj)


# ❌ YAML DESERIALIZATION (CRITICAL)
@app.route("/yaml", methods=["POST"])
def yaml_load():
    data = request.data
    return str(yaml.load(data, Loader=yaml.Loader))


# ❌ PATH TRAVERSAL (HIGH)
@app.route("/read")
def read_file():
    filename = request.args.get("file")
    with open(filename, "r") as f:
        return f.read()


# ❌ FILE WRITE (HIGH)
@app.route("/write", methods=["POST"])
def write_file():
    filename = request.args.get("file")
    content = request.data.decode()

    with open(filename, "w") as f:
        f.write(content)

    return "written"


# ❌ SSRF (HIGH)
@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    response = requests.get(url)
    return response.text


# ❌ OPEN REDIRECT (MEDIUM)
@app.route("/redirect")
def redirect():
    url = request.args.get("url")
    from flask import redirect as flask_redirect
    return flask_redirect(url)


# ❌ WEAK AUTH (HIGH)
@app.route("/admin")
def admin():
    token = request.args.get("token")

    if token == "admin123":  # hardcoded auth
        return "Welcome admin"
    return "Unauthorized"


# ❌ BASE64 “ENCRYPTION” (BAD PRACTICE)
@app.route("/encode")
def encode():
    data = request.args.get("data")
    return base64.b64encode(data.encode()).decode()


# ❌ NO AUTH FILE UPLOAD (HIGH)
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save("/tmp/" + file.filename)
    return "uploaded"


# ❌ DIRECTORY LISTING (INFO DISCLOSURE)
@app.route("/list")
def list_files():
    path = request.args.get("path", ".")
    return str(os.listdir(path))


# ❌ DEBUG ENABLED (CRITICAL IN PROD)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
