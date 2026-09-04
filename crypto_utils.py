from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()

    with open("secret.key", "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists("secret.key"):
        generate_key()

    with open("secret.key", "rb") as file:
        return file.read()

CIPHER = Fernet(load_key())

def encrypt_password(password: str) -> bytes:
    return CIPHER.encrypt(password.encode()) #encrypt expects bytes not string


def decrypt_password(token: bytes) -> str:
    return CIPHER.decrypt(token).decode()
# we only have the key, we need to provide this key to a lock which will be unique to the keys and use that lock to encrypt and decrypt the data
