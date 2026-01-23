import strawberry
from strawberry.types import Info

from app.application.quote_service import QuoteService
from app.domain.quotes import InvalidConsumptionError
from app.domain.quotes import StateNotFoundError
from app.adapters.graphql.context import GraphQLContext
from app.adapters.graphql.errors import as_graphql_error
from app.adapters.graphql.types import SolutionQuoteType
from app.adapters.graphql.types import StateQuoteType
from app.adapters.graphql.types import StateType
from app.adapters.graphql.types import SupplierQuoteType
from app.infrastructure.db.models import State
from app.infrastructure.repositories.sqlalchemy_quote_repository import SqlAlchemyQuoteRepository


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    def states(self, info: Info[GraphQLContext, None]) -> list[StateType]:
        session = info.context.db
        states = session.query(State).order_by(State.code).all()
        return [
            StateType(code=state.code, name=state.name, base_tariff_per_kwh=state.base_tariff_per_kwh)
            for state in states
        ]

    @strawberry.field
    def quote(
        self,
        info: Info[GraphQLContext, None],
        state_code: str,
        consumption_kwh: float,
    ) -> StateQuoteType:
        session = info.context.db
        repo = SqlAlchemyQuoteRepository(session)
        service = QuoteService(repo)
        try:
            quote = service.build_state_quote(state_code=state_code, consumption_kwh=consumption_kwh)
        except (StateNotFoundError, InvalidConsumptionError) as exc:
            raise as_graphql_error(exc) from exc
        except Exception as exc:
            raise as_graphql_error(exc) from exc

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
