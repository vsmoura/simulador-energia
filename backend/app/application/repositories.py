from __future__ import annotations

from typing import Protocol

from app.domain.entities import State
from app.domain.entities import SupplierAvailability


class QuoteRepository(Protocol):
    def get_state(self, state_code: str) -> State | None:
        ...

    def get_supplier_availabilities(self, state_code: str) -> list[SupplierAvailability]:
        ...
    def list_states(self) -> list[State]:
        ...
