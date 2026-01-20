from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.seed import seed_database
from app.domain.models import SolutionType
from app.domain.services import InvalidConsumptionError
from app.domain.services import StateNotFoundError
from app.domain.services import build_state_quote


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_build_state_quote_returns_ranked_solutions() -> None:
    session = _session()
    seed_database(session)

    quote = build_state_quote(session, state_code="SP", consumption_kwh=30000)

    assert quote.state_code == "SP"
    assert quote.base_cost > 0
    assert {solution.solution_type for solution in quote.solutions} == {
        SolutionType.GD,
        SolutionType.MERCADO_LIVRE,
    }
    for solution in quote.solutions:
        assert solution.best_economy >= 0
        assert solution.suppliers
        assert solution.suppliers[0].economy >= solution.suppliers[-1].economy


def test_build_state_quote_invalid_consumption() -> None:
    session = _session()
    seed_database(session)

    try:
        build_state_quote(session, state_code="SP", consumption_kwh=0)
    except InvalidConsumptionError:
        assert True
    else:
        assert False, "Expected InvalidConsumptionError"


def test_build_state_quote_unknown_state() -> None:
    session = _session()
    seed_database(session)

    try:
        build_state_quote(session, state_code="XX", consumption_kwh=1000)
    except StateNotFoundError:
        assert True
    else:
        assert False, "Expected StateNotFoundError"
