from typing import Optional
from sqlalchemy.orm import DeclarativeBase , mapped_column, Mapped
from sqlalchemy import DateTime,Boolean,MetaData
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
    """
    declarative base class for all models
    """
    __abstract__ = True

    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(), onupdate=func.now(), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    