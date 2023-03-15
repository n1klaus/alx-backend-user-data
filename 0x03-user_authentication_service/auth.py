#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt
from db import DB
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    """Returns a hashed password"""
    if password:
        salt: bytes = bcrypt.gensalt()
        hashed_pw: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_pw
    return None


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Instantiates database instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """Registers and returns a new user from credentials"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except BaseException:
            pass
        if user:
            raise ValueError(f"User {email} already exists.")
        hashed_pw: bytes = _hash_password(password)
        user = self._db.add_user(email, hashed_pw)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user exists and with correct password"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except BaseException:
            pass
        if user is None:
            return False
        if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
            return True
        return False
