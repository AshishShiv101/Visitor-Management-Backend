import datetime
from sqlalchemy import Column, func, text
from sqlalchemy.types import Boolean, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True


class ModelBase(Base):
    """
    Model Base class with created_at and updated_at functionality.
    - To be used across all tables in the database.
    """

    __abstract__ = True

    created_at = Column(
        DateTime,
        server_default = func.now(),
        default = datetime.datetime.now,
        nullable = False,
        doc = "Entry created at",
        comment = "Row created at",
    )

    updated_at = Column(
        DateTime,
        server_default = func.now(),
        default = datetime.datetime.now,
        onupdate = datetime.datetime.now,
        nullable = False,
        doc = "Entry last updated",
        comment = "Row last updated",
    )