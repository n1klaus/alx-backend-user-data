#!/usr/bin/env python3
"""
Module for basic authentication handling
"""

from api.v1.auth.auth import Auth
import base64
import re
from typing import Tuple


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
            not ":" in decoded_base64_authorization_header:
            return None, None
        return tuple(re.split(":", decoded_base64_authorization_header))
