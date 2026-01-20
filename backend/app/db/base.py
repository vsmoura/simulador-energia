from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# Import models to ensure they are registered with the metadata.
from app.domain import models  # noqa: F401,E402
