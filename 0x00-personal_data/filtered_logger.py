#!/usr/bin/env python3
"""Use a regex to replace occurrences of certain field values."""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Args:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field
            will be obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by which character
            is separating all fields in the log line (message)
    Returns:
        (str): the log message obfuscated
    """
    for field in fields:
        sub: str = re.search(f"(?<={field}=).*?(?={separator})",
                             message, re.IGNORECASE)
        message = re.sub(sub.group(0), redaction, message) if sub else None
    return message
