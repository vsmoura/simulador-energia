import strawberry
from strawberry.exceptions import GraphQLError
from strawberry.types import Info

from app.domain.models import State
from app.domain.services import InvalidConsumptionError
from app.domain.services import StateNotFoundError
from app.domain.services import build_state_quote
from app.graphql.types import SolutionQuoteType
from app.graphql.types import StateQuoteType
from app.graphql.types import StateType
from app.graphql.types import SupplierQuoteType


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    def states(self, info: Info) -> list[StateType]:
        session = info.context["db"]
        states = session.query(State).order_by(State.code).all()
        return [
            StateType(code=state.code, name=state.name, base_tariff_per_kwh=state.base_tariff_per_kwh)
            for state in states
        ]

    @strawberry.field
    def quote(self, info: Info, state_code: str, consumption_kwh: float) -> StateQuoteType:
        session = info.context["db"]
        try:
            quote = build_state_quote(session, state_code=state_code, consumption_kwh=consumption_kwh)
        except StateNotFoundError as exc:
            raise GraphQLError(str(exc)) from exc
        except InvalidConsumptionError as exc:
            raise GraphQLError(str(exc)) from exc

        solutions = []
        for solution in quote.solutions:
            suppliers = [
                SupplierQuoteType(
                    supplier_id=entry.supplier_id,
                    supplier_name=entry.supplier_name,
                    supplier_logo_url=entry.supplier_logo_url,
                    supplier_origin_state=entry.supplier_origin_state,
                    total_customers=entry.total_customers,
                    average_rating=entry.average_rating,
                    solution_type=entry.solution_type,
                    cost_per_kwh=entry.cost_per_kwh,
                    cost_total=entry.cost_total,
                    economy=entry.economy,
                    economy_percent=entry.economy_percent,
                )
                for entry in solution.suppliers
            ]
            solutions.append(
                SolutionQuoteType(
                    solution_type=solution.solution_type,
                    best_economy=solution.best_economy,
                    best_economy_percent=solution.best_economy_percent,
                    suppliers=suppliers,
                )
            )
        return StateQuoteType(
            state_code=quote.state_code,
            state_name=quote.state_name,
            base_tariff_per_kwh=quote.base_tariff_per_kwh,
            consumption_kwh=quote.consumption_kwh,
            base_cost=quote.base_cost,
            solutions=solutions,
        )


schema = strawberry.Schema(query=Query)