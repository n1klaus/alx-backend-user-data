#!/usr/bin/env python
""" Module of session authentication views
"""

from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, Response
import os

@app_views.route("/auth_session/login", methods=["POST"],
                  strict_slashes=False)
def session_login() -> Response:
    """Handles session authentication"""
    email: str = request.form.get("email")
    if not email:
        return { "error": "email missing" }, 400
    password: str = request.form.get("password")
    if not password:
        return { "error": "password missing" }, 400
    user_list: list = User.search({"email": email})
    if not user_list:
        return { "error": "no user found for this email" }, 404
    user: User = user_list[0]
    if not user.is_valid_password(password):
        return { "error": "wrong password" }, 401
    from api.v1.app import auth
    session_id: str = auth.create_session(user.id)
    response: Response = jsonify(user.to_json())
    SESSION_NAME: str = os.getenv("SESSION_NAME")
    response.set_cookie(SESSION_NAME, session_id)
    return response