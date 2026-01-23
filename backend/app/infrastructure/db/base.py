from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


from app.infrastructure.db import models  # noqa: F401,E402
