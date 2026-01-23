import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.seed import seed_database
from app.graphql.context import GraphQLContext


def _session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


@pytest.fixture
def build_session():
    session = _session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def build_context():
    session = _session()
    seed_database(session)
    try:
        yield GraphQLContext(db=session)
    finally:
        session.close()
