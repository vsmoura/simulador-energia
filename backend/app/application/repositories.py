from __future__ import annotations

from typing import Protocol

from app.domain.quotes import SolutionType
from app.infrastructure.db.models import SupplierAvailability
from app.infrastructure.db.models import State


class QuoteRepository(Protocol):
    def get_state_with_suppliers(self, state_code: str) -> State | None:
        ...

    def get_supplier_availabilities(self, state: State) -> list[SupplierAvailability]:
        ...

    def get_solution_cost(self, availability: SupplierAvailability) -> float | None:
        ...

    def get_solution_type(self, availability: SupplierAvailability) -> SolutionType:
        ...
