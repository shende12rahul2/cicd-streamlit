import streamlit as st
import sqlite3
import subprocess
import os
import pickle
import yaml
import requests

st.title("⚠️ Vulnerable Streamlit Demo App")

# ❌ Hardcoded secret (HIGH)
SECRET_KEY = "streamlit-secret-123"


# ❌ SQL Injection (HIGH)
st.header("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    result = cursor.fetchall()
    st.write(result)


# ❌ Command Injection (CRITICAL)
st.header("Run Command")
cmd = st.text_input("Enter command")

if st.button("Execute"):
    output = subprocess.check_output(cmd, shell=True)
    st.text(output.decode())


# ❌ Eval Injection (CRITICAL)
st.header("Eval Code")
code = st.text_area("Enter Python code")

if st.button("Run Eval"):
    result = eval(code)
    st.write(result)


# ❌ Path Traversal (HIGH)
st.header("Read File")
file_path = st.text_input("Enter file path")

if st.button("Read"):
    with open(file_path, "r") as f:
        st.text(f.read())


# ❌ Insecure Deserialization (CRITICAL)
st.header("Deserialize Pickle")
uploaded_file = st.file_uploader("Upload pickle file")

if uploaded_file:
    data = uploaded_file.read()
    obj = pickle.loads(data)
    st.write(obj)


# ❌ YAML Deserialization (CRITICAL)
st.header("YAML Load")
yaml_input = st.text_area("Paste YAML")

if st.button("Load YAML"):
    parsed = yaml.load(yaml_input, Loader=yaml.Loader)
    st.write(parsed)


# ❌ SSRF (HIGH)
st.header("Fetch URL")
url = st.text_input("Enter URL")

if st.button("Fetch"):
    response = requests.get(url)
    st.text(response.text[:500])


# ❌ OS Command (CRITICAL)
st.header("OS Command")
os_cmd = st.text_input("OS command")

if st.button("Run OS"):
    os.system(os_cmd)


# ❌ Weak Auth (HIGH)
st.header("Admin Access")
token = st.text_input("Enter admin token")

if st.button("Access"):
    if token == "admin123":
        st.success("Welcome Admin")
    else:
        st.error("Unauthorized")
