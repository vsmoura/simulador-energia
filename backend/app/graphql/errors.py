from __future__ import annotations

from strawberry.exceptions import GraphQLError

from app.domain.services import InvalidConsumptionError
from app.domain.services import StateNotFoundError


def as_graphql_error(error: Exception) -> GraphQLError:
    if isinstance(error, StateNotFoundError):
        return GraphQLError(str(error), extensions={"code": "STATE_NOT_FOUND"})
    if isinstance(error, InvalidConsumptionError):
        return GraphQLError(str(error), extensions={"code": "INVALID_CONSUMPTION"})
    return GraphQLError("Unexpected error.", extensions={"code": "UNEXPECTED_ERROR"})
