"""auth-service: sign-in checks."""

import hashlib


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode()).hexdigest()


def check_login(email: str, password: str, user: dict) -> bool:
    """user: {"email", "salt", "password_hash"} as stored. Emails are case-insensitive."""
    if email.strip().lower() != user["email"].lower():
        return False
    return hash_password(password, user["salt"]) == user["password_hash"]
