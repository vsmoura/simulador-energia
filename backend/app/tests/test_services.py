from sqlalchemy.orm import Session

from app.application.quote_service import QuoteService
from app.infrastructure.db.seed import seed_database
from app.domain.quotes import InvalidConsumptionError
from app.domain.quotes import SolutionType
from app.domain.quotes import StateNotFoundError
from app.infrastructure.repositories.sqlalchemy_quote_repository import SqlAlchemyQuoteRepository


def test_build_state_quote_returns_ranked_solutions(build_session) -> None:
    session: Session = build_session
    seed_database(session)
    service = QuoteService(SqlAlchemyQuoteRepository(session))

    quote = service.build_state_quote(state_code="SP", consumption_kwh=30000)

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
    service = QuoteService(SqlAlchemyQuoteRepository(session))

    try:
        service.build_state_quote(state_code="SP", consumption_kwh=0)
    except InvalidConsumptionError:
        assert True
    else:
        assert False, "Expected InvalidConsumptionError"


def test_build_state_quote_unknown_state(build_session) -> None:
    session: Session = build_session
    seed_database(session)
    service = QuoteService(SqlAlchemyQuoteRepository(session))

    try:
        service.build_state_quote(state_code="XX", consumption_kwh=1000)
    except StateNotFoundError:
        assert True
    else:
        assert False, "Expected StateNotFoundError"
