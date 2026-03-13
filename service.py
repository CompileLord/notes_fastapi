import secrets
import hashlib

def generate_token():
    token = secrets.token_urlsafe(32)
    return token

def hash_password(password: str):
    hashed = hashlib.sha256(password.encode())
    print(str(hashed))
    return hashed.hexdigest()