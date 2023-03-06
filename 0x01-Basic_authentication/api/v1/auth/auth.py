#!/usr/bin/env python3
"""
Module for authentication handling
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for path"""
        if path is None or not excluded_paths:
            return True
        if (path or f"{path}/") in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns authorization header from a request if available"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns authorized user from a request if available"""
        return None
