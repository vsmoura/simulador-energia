from sqlalchemy.orm import Session

from app.db.seed import seed_database
from app.domain.models import SolutionType
from app.domain.services import InvalidConsumptionError
from app.domain.services import StateNotFoundError
from app.domain.services import build_state_quote


def test_build_state_quote_returns_ranked_solutions(build_session) -> None:
    session: Session = build_session
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


def test_build_state_quote_invalid_consumption(build_session) -> None:
    session: Session = build_session
    seed_database(session)

    try:
        build_state_quote(session, state_code="SP", consumption_kwh=0)
    except InvalidConsumptionError:
        assert True
    else:
        assert False, "Expected InvalidConsumptionError"


def test_build_state_quote_unknown_state(build_session) -> None:
    session: Session = build_session
    seed_database(session)

    try:
        build_state_quote(session, state_code="XX", consumption_kwh=1000)
    except StateNotFoundError:
        assert True
    else:
        assert False, "Expected StateNotFoundError"
