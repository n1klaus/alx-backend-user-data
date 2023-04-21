#!/usr/bin/env python3
"""
Module for session authentication handling
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta

SESSION_DURATION = os.getenv("SESSION_DURATION", None)


class SessionExpAuth(SessionAuth):
    """Session authentication scheme with expiry"""

    def __init__(self):
        """Initializes instances with required attributes"""
        try:
            self.session_duration = int(SESSION_DURATION)
        except BaseException:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user id"""
        if not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        if user_id is None:
            return None
        session_dictionary = {
            "user_id ": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on session_id"""
        if not isinstance(session_id, str) or \
                not isinstance(self.user_id_by_session_id, dict):
            return None
        sd = self.user_id_by_session_id.get(session_id)
        if sd is None or "created_at" not in sd:
            return None
        if self.session_duration <= 0:
            return sd.get("user_id")
        if sd.get("created_at") + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None
        return sd.get("user_id")
