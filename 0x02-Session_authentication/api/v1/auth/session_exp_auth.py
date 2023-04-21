#!/usr/bin/env python3
"""
Module for basic authentication handling
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta

SESSION_DURATION = os.getenv("SESSION_DURATION", None)


class SessionExpAuth(SessionAuth):
    """"""

    def __init__(self):
        """"""
        try:
            self.session_duration = int(SESSION_DURATION)
        except BaseException:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)
        if user_id is None:
            return None
        session_dictionary = {
            "user_id ": user_id,
            "created_at": datetime.now()
        }
        SessionExpAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user_id based on session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        sd = SessionExpAuth.user_id_by_session_id.get(session_id)
        if sd is None or self.session_duration > 0 or \
            "created_at" not in sd or sd.get("created_at") + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None
        return sd.get("user_id")
