import secrets
import string

def generate_password():
    pool = string.ascii_letters + string.digits + string.punctuation

    return "".join(secrets.choice(pool) for _ in range(16))

