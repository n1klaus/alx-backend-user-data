#!/usr/bin/env python3
"""Use a regex to replace occurrences of certain field values."""

import logging
from mysql.connector import connection, Error
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
        sub: str = re.search(f"(?<={field}=).*?(?={separator})", message)
        message = re.sub(sub.group(0), redaction, message) if sub else message
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
        msg: str = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            msg, self.SEPARATOR)


PII_FIELDS: tuple = ("email", "name", "phone", "password", "ssn")

DBCONFIG = {
    "user": os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
    "password": os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    "host": os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
    "database": os.getenv("PERSONAL_DATA_DB_NAME"),
    "raise_on_warnings": True
}


def get_db() -> connection.MySQLConnection:
    """Returns connector to the database"""
    try:
        connector = connection.MySQLConnection(**DBCONFIG)
    except Error:
        raise
    return connector


def main() -> None:
    """
    Retrieves all rows in the users table
    and displays each row under a filtered format
    """
    logger: logging.Logger = get_logger()
    db: connection.MySQLConnection = get_db()
    curs = db.cursor()
    curs.execute("SELECT * FROM users;")
    for name, email, phone, ssn, password, ip, last_login, user_agent in curs:
        mapping = {
            "name": name,
            "email": email,
            "phone": phone,
            "ssn": ssn,
            "password": password,
            "ip": ip,
            "last_login": last_login,
            "user_agent": user_agent
        }
        logger.log(logger.getEffectiveLevel(), **mapping)
    curs.close()
    db.close()


if __name__ == "__main__":
    main()
