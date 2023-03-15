#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns a hashed password"""
    if password:
        salt: bytes = bcrypt.gensalt()
        hashed_pw: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_pw
    return None
