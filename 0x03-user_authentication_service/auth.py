#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt
from db import DB
from typing import TypeVar
from uuid import uuid4, UUID
from user import User


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

    def register_user(self, email: str, password: str) -> User:
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

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns user from session id"""
        if session_id is None:
            return None
        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except BaseException:
            pass
        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session id to None"""
        if user_id is None or not isinstance(user_id, int):
            return
        try:
            self._db.update_user(user_id, session_id=None)
        except BaseException:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Returns generated reset token from user's email"""
        if email is None:
            return
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token: str = _generate_uuid()
                self._db.update_user(user.id, reset_token=token)
                return token
        except BaseException:
            pass
        raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates user password"""
        if reset_token is None or password is None:
            return None
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_pw: bytes = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hash_pw,
                reset_token=None)
        except BaseException:
            raise ValueError
