from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.seed import seed_database
from app.graphql.context import GraphQLContext
from app.graphql.schema import schema


def _context() -> GraphQLContext:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    seed_database(session)
    return GraphQLContext(db=session)


def test_states_query_returns_data() -> None:
    query = """
        query {
            states {
                code
                name
                baseTariffPerKwh
            }
        }
    """
    result = schema.execute_sync(query, context_value=_context())

    assert result.errors is None
    assert result.data["states"]


def test_quote_query_returns_solutions() -> None:
    query = """
        query GetQuote($stateCode: String!, $consumptionKwh: Float!) {
            quote(stateCode: $stateCode, consumptionKwh: $consumptionKwh) {
                stateCode
                baseCost
                solutions {
                    solutionType
                    bestEconomy
                }
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"stateCode": "SP", "consumptionKwh": 30000},
        context_value=_context(),
    )

    assert result.errors is None
    assert result.data["quote"]["solutions"]


def test_quote_query_invalid_consumption_returns_error() -> None:
    query = """
        query GetQuote($stateCode: String!, $consumptionKwh: Float!) {
            quote(stateCode: $stateCode, consumptionKwh: $consumptionKwh) {
                stateCode
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"stateCode": "SP", "consumptionKwh": 0},
        context_value=_context(),
    )

    assert result.errors
    assert result.errors[0].extensions["code"] == "INVALID_CONSUMPTION"
