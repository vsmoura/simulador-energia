from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.application.repositories import QuoteRepository
from app.domain.entities import State as DomainState
from app.domain.entities import Supplier as DomainSupplier
from app.domain.entities import SupplierAvailability as DomainSupplierAvailability
from app.infrastructure.db.models import State
from app.infrastructure.db.models import Supplier
from app.infrastructure.db.models import SupplierAvailability


class SqlAlchemyQuoteRepository(QuoteRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_state(self, state_code: str) -> DomainState | None:
        state = (
            self.session.query(State)
            .filter(State.code == state_code)
            .one_or_none()
        )
        if state is None:
            return None
        return DomainState(
            code=state.code,
            name=state.name,
            base_tariff_per_kwh=state.base_tariff_per_kwh,
        )

    def list_states(self) -> list[DomainState]:
        states = self.session.query(State).order_by(State.code).all()
        return [
            DomainState(code=state.code, name=state.name, base_tariff_per_kwh=state.base_tariff_per_kwh)
            for state in states
        ]

    def get_supplier_availabilities(self, state_code: str) -> list[DomainSupplierAvailability]:
        state = (
            self.session.query(State)
            .options(
                selectinload(State.suppliers)
                .selectinload(SupplierAvailability.supplier)
                .selectinload(Supplier.solutions),
                selectinload(State.suppliers)
                .selectinload(SupplierAvailability.supplier)
                .selectinload(Supplier.origin_state),
            )
            .filter(State.code == state_code)
            .one_or_none()
        )
        if state is None:
            return []
        availabilities: list[DomainSupplierAvailability] = []
        for availability in state.suppliers:
            supplier = availability.supplier
            solution = next(
                (solution for solution in supplier.solutions if solution.solution_type == availability.solution_type),
                None,
            )
            if solution is None:
                continue
            domain_supplier = DomainSupplier(
                id=supplier.id,
                name=supplier.name,
                logo_url=supplier.logo_url,
                origin_state_code=supplier.origin_state.code,
                total_customers=supplier.total_customers,
                average_rating=supplier.average_rating,
            )
            availabilities.append(
                DomainSupplierAvailability(
                    supplier=domain_supplier,
                    solution_type=availability.solution_type,
                    cost_per_kwh=solution.cost_per_kwh,
                )
            )
        return availabilities
