from strawberry.exceptions import GraphQLError

from app.domain.quotes import InvalidConsumptionError
from app.domain.quotes import StateNotFoundError
from app.graphql.errors import as_graphql_error

def test_as_graphql_error_state_not_found() -> None:
    error = as_graphql_error(StateNotFoundError("State XX not found."))

    assert isinstance(error, GraphQLError)
    assert error.extensions == {"code": "STATE_NOT_FOUND"}


def test_as_graphql_error_invalid_consumption() -> None:
    error = as_graphql_error(InvalidConsumptionError("Consumption must be greater than zero."))

    assert isinstance(error, GraphQLError)
    assert error.extensions == {"code": "INVALID_CONSUMPTION"}


def test_as_graphql_error_unexpected() -> None:
    error = as_graphql_error(RuntimeError("boom"))

    assert isinstance(error, GraphQLError)
    assert error.extensions == {"code": "UNEXPECTED_ERROR"}
