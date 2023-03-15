#!/usr/bin/env python3
"""Basic Flask app"""

from auth import Auth
from flask import Flask, jsonify, request


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
