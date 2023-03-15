#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt
from db import DB
from typing import TypeVar
from uuid import uuid4, UUID


def _hash_password(password: str) -> bytes:
    """Returns a hashed password"""
    if password:
        salt: bytes = bcrypt.gensalt()
        hashed_pw: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_pw
    return None


def _generate_uuid() -> str:
    """Returns a random uuid"""
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """
        Returns the generated user's session id with the user
        corresponding to the email in the database
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except BaseException:
            pass
        if user:
            session_id: str = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
