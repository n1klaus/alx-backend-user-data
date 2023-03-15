#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Returns the created user object"""
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        try:
            self._session.add(user)
            self._session.commit()
        except BaseException:
            pass
        return user

    def find_user_by(self, **kwargs) -> User:
        """Returns the first result of the user object"""
        if kwargs:
            user: User = self._session.query(User) \
                .filter_by(**kwargs) \
                .first()
            if user:
                return user
            raise NoResultFound
        raise InvalidRequestError
