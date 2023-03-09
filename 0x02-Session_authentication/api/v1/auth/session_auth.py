#!/usr/bin/env python3
"""
Module for session authentication handling
"""

from api.v1.auth.auth import Auth
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
