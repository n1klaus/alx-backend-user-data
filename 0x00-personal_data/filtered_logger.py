#!/usr/bin/env python3
"""Use a regex to replace occurrences of certain field values."""

import logging
import mysql.connector
import os
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


def get_logger() -> logging.Logger:
    """
    Returns a logger object
    """
    logging.basicConfig(level=logging.INFO, encoding="utf-8")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger = logging.getLogger("user_data")
    logger.addHandler(handler)
    logger.propagate = False
    return logger


DBCONFIG = {
    "user": os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
    "password": os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    "host": os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
    "database": os.getenv("PERSONAL_DATA_DB_NAME"),
    "raise_on_warnings": True
}


def get_db():
    """Returns connector to the database"""
    try:
        connector = mysql.connector.connection.MySQLConnection(**DBCONFIG)
    except mysql.connector.Error:
        raise
    return connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes format parameters"""
        super(RedactingFormatter, self).__init__(fmt=self.FORMAT)
        self.fields: list = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns formatted record message with format settings"""
        msg: str = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR)
        return (self.FORMAT) % {"name": record.name, "message": msg,
                                "levelname": record.levelname,
                                "asctime": self.formatTime(record)}


PII_FIELDS: tuple = ("email", "ip", "phone", "password", "ssn")
