from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.application.repositories import QuoteRepository
from app.domain.quotes import SolutionType
from app.infrastructure.db.models import State
from app.infrastructure.db.models import Supplier
from app.infrastructure.db.models import SupplierAvailability


class SqlAlchemyQuoteRepository(QuoteRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_state_with_suppliers(self, state_code: str) -> State | None:
        return (
            self.session.query(State)
            .options(
                selectinload(State.suppliers)
                .selectinload(SupplierAvailability.supplier)
                .selectinload(Supplier.solutions)
            )
            .filter(State.code == state_code)
            .one_or_none()
        )

    def get_supplier_availabilities(self, state: State) -> list[SupplierAvailability]:
        return list(state.suppliers)

    def get_solution_cost(self, availability: SupplierAvailability) -> float | None:
        supplier = availability.supplier
        solution = next(
            (solution for solution in supplier.solutions if solution.solution_type == availability.solution_type),
            None,
        )
        return None if solution is None else solution.cost_per_kwh

    def get_solution_type(self, availability: SupplierAvailability) -> SolutionType:
        return availability.solution_type
