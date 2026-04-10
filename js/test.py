import hashlib
import os
import random
import tempfile


# MEDIUM: insecure randomness
def generate_token():
    return str(random.random())


# MEDIUM: command injection
def run_cmd(user_input):
    os.system("echo " + user_input)


# MEDIUM: hardcoded password
def connect():
    password = "admin123"
    return password


# LOW: weak hashing
def weak_hash(data):
    return hashlib.md5(data.encode()).hexdigest()


# LOW: insecure temp file
def create_temp():
    return tempfile.mktemp()


# LOW: improper assert
def check_age(age):
    assert age > 18


if __name__ == "__main__":
    print(generate_token())
    run_cmd("hello")
    print(connect())
    print(weak_hash("test"))
    print(create_temp())
    check_age(10)
