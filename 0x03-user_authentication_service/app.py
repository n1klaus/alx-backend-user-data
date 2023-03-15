#!/usr/bin/env python3
"""Basic Flask app"""

from auth import Auth
from flask import Flask, jsonify, request, abort, Response, redirect, url_for


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def root():
    """Root Endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """User registration endpoint"""
    email: str = request.form.get("email")
    password: str = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": email,
                            "message": "user created"})
        raise
    except BaseException:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Session login endpoint"""
    email: str = request.form.get("email")
    password: str = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id: str = AUTH.create_session(email)
        resp: Response = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie(key="session_id", value=session_id)
        return resp
    abort(401)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """User profile data endpoint"""
    session_id: str = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Session logout endpoint"""
    session_id: str = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for(root))
    abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """"""
    email: str = request.form.get("email")
    password: str = request.form.get("new_password")
    reset_token: str = request.form.get("reset_token")
    if email and password and reset_token:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Reset password endpoint"""
    email: str = request.form.get("email")
    if email:
        token: str = AUTH.get_reset_password_token(email)
        if token:
            return jsonify(
                {"email": email,
                 "reset_token": token
                 }
            ), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
