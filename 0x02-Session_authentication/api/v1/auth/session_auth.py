#!/usr/bin/env python3
"""
Module for session authentication handling
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """Session authentication scheme"""
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id: str = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns a user instance based on a cookie value"""
        session_id: str = self.session_cookie(request)
        if session_id:
            user_id: str = SessionAuth.user_id_by_session_id.get(session_id)
            return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session on logout"""
        if request is None:
            return False
        session_id: str = self.session_cookie(request)
        if session_id is None:
            return False
        user_id: str = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
