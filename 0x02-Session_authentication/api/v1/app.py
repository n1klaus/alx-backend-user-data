#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.getenv("AUTH_TYPE", None):
    if os.getenv("AUTH_TYPE") == "basic_auth":
        auth = BasicAuth()
    elif os.getenv("AUTH_TYPE") == "session_auth":
        auth = SessionAuth()
    else:
        auth = Auth()

TRUSTED_PATHS = [
    '/api/v1/status/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/',
    '/api/v1/auth_session/login/'
]


@app.before_request
def preliminaries() -> None:
    """Checks if authentication is required and meets the requirements"""
    if auth is not None:
        if auth.require_auth(request.path, TRUSTED_PATHS):
            if not auth.authorization_header(request) or \
                not auth.session_cookie(request):
                abort(401)
            if not auth.current_user(request):
                abort(403)
            request.current_user = auth.current_user(request)


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized error handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """ Not allowed access error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
