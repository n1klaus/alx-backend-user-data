#!/usr/bin/env python3
"""
Module for session authentication handling
"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session authentication scheme with database storage"""

    def create_session(self, user_id=None):
        """Creates a session id for a user id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**session_dictionary)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user_id based on session_id"""
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """Deletes the user session on logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
