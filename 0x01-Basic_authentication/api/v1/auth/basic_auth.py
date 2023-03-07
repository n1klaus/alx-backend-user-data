#!/usr/bin/env python3
"""
Module for basic authentication handling
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
import re
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """Basic authentication scheme"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns base64 part of authorization header"""
        if authorization_header is None or \
            not isinstance(authorization_header, str) or \
                not re.search("Basic\\s.*", authorization_header):
            return None
        result: str = re.search("(?<=Basic\\s).*", authorization_header)
        return str(result.group(0))

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """Returns the decoded value of a Base64 string"""
        try:
            if base64_authorization_header is None or \
                    not isinstance(base64_authorization_header, str):
                return None
            if re.search("Basic\\s.*", base64_authorization_header):
                result: str = re.search("(?<=Basic\\s).*",
                                        base64_authorization_header)
                base64_string: str = result.group(0)
            else:
                base64_string: str = base64_authorization_header.strip()
            decoded_string: bytes = base64.b64decode(base64_string)
            return decoded_string.decode("utf-8")
        except BaseException:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> Tuple[str, str]:
        """Returns the user email and password from base64 decoded value"""
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(re.split(":", decoded_base64_authorization_header))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        """Returns user instance based on his email and password"""
        if user_email is None or user_pwd is None or \
                not isinstance(user_email or user_pwd, str):
            return None
        if User.count() == 0:
            return None
        result: list = User.search({"email": user_email})
        if len(result) == 0:
            return None
        for _user in result:
            if _user.is_valid_password(user_pwd):
                return _user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user instance for a request"""
        auth_header: str = self.authorization_header(request)
        if auth_header:
            base64_string: str = self \
                .extract_base64_authorization_header(auth_header)
            if base64_string:
                decoded_string: str = self \
                    .decode_base64_authorization_header(base64_string)
                if decoded_string:
                    email, password = self \
                        .extract_user_credentials(decoded_string)
                    if email and password:
                        user: User = self \
                            .user_object_from_credentials(email, password)
                        return user
        return None
