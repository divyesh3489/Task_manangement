"""
Dependency functions for the API.
"""
from typing import Generator
from sqlalchemy.orm import Session
from db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session
    
    :return: Description
    :rtype: Generator[Session, None, None]
    """
    try:
        db : Session = SessionLocal()
        yield db
    finally:
        db.close()

    