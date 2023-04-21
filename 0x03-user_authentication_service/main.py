#!/usr/bin/env python3
"""Perform an end-to-end integration test of user authentication."""
import requests


URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test the `/users endpoint` of the application.
    Args:
        email (str): user's email.
        password (str): user's password.
    """
    resp = requests.post(
        f"{URL}/users",
        data={
            'email': email,
            'password': password})
    if resp.status_code == 200:
        assert resp.json() == {"email": f"{email}", "message": "user created"}
    else:
        assert resp.status_code == 401


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login functionality having provided the wrong credentials.
    Args:
        email (str): user's email address.
        password (str): user's password.
    """
    resp = requests.post(
        f'{URL}/sessions',
        data={
            'email': email,
            'password': password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login functionality with the right credentials.
    Args:
        email (str): user's email address.
        password (str): user's password.
    """
    resp = requests.post(
        f'{URL}/sessions',
        data={
            'email': email,
            'password': password})
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'logged in'}
    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test getting a user's profile while not logged in."""
    resp = requests.get(f'{URL}/profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test getting a user's profile while logged in.
    Args:
        session_id (str): session id corresponding to a logged in user.
    """
    resp = requests.get(f'{URL}/profile', cookies={'session_id': session_id})
    assert resp.status_code == 200
    assert 'email' in resp.json()


def log_out(session_id: str) -> None:
    """Test logged out functionality.
    Args:
        session_id (str): session id to expire.
    """
    resp = requests.delete(
        f'{URL}/sessions',
        cookies={
            'session_id': session_id})
    if resp.status_code == 302:
        assert resp.url == f'{URL}/'
    else:
        assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """Test password reset functionality.
    Args:
        email (str): user's email address.
    """
    resp = requests.post(f'{URL}/reset_password', data={'email': email})
    if resp.status_code == 200:
        return resp.json().get('reset_token')
    assert resp.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update password functionality.
    Args:
        email (str): user's email address.
        reset_token (str): reset token for specific user.
        new_password (str): user's new password.
    """
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    resp = requests.put(f'{URL}/reset_password', data=data)
    if resp.status_code == 200:
        assert resp.json() == {"email": email,
                               "message": "Password updated"}
    else:
        assert resp.status_code == 403


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
