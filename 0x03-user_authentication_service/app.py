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
    """User login endpoint"""
    email: str = request.form.get("email")
    password: str = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_id: str = AUTH.create_session(email)
        resp: Response = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie(key="session_id", value=session_id)
        return resp
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Deletes session id associated with user"""
    session_id: str = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for(root))
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
