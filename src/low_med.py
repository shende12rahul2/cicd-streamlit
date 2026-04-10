import hashlib
import random
import tempfile


# MEDIUM: Insecure Randomness
def generate_discount_code():
    # Rule: py/insecure-randomness
    code = random.randint(1000, 9999)
    return str(code)


# LOW: Insecure Temporary File & Weak Cryptography
def create_temp_hash(data):
    # Rule: py/weak-crypto
    weak_hash = hashlib.sha1(data.encode()).hexdigest()

    # Rule: py/insecure-temporary-file
    tmp = tempfile.mktemp()  # noqa: F841
    return weak_hash


# LOW: Empty Except Block
def parse_data(raw_data):
    try:
        parsed = int(raw_data)
        return parsed
    except Exception:  # noqa: E722
        # Rule: py/empty-except
        pass
    return 0


if __name__ == "__main__":
    print(generate_discount_code())
    print(create_temp_hash("test_data"))
    print(parse_data("abc"))
