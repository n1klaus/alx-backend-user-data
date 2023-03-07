#!/usr/bin/env python3
"""
Module for basic authentication handling
"""

from api.v1.auth.auth import Auth
import re


class BasicAuth(Auth):
    """Basic authentication scheme"""
    
    def extract_base64_authorization_header(self, 
                                            authorization_header: str) -> str:
        """Returns base64 part of authorization header"""
        if authorization_header is None or \
            not isinstance(authorization_header, str) or \
                not re.search("Basic\s.*", authorization_header):
            return None
        result: str = re.search("(?<=Basic\s).*", authorization_header)
        return str(result.group(0))
