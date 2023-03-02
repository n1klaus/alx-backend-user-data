#!/usr/bin/env python3
"""Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted and hashed password byte string"""
    salt: bytes = bcrypt.gensalt()
    hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the encrypted password matches provided password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
