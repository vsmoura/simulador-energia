from __future__ import annotations

from dataclasses import dataclass

from app.domain.quotes import SolutionType


@dataclass(frozen=True)
class State:
    code: str
    name: str
    base_tariff_per_kwh: float


@dataclass(frozen=True)
class Supplier:
    id: int
    name: str
    logo_url: str
    origin_state_code: str
    total_customers: int
    average_rating: float


@dataclass(frozen=True)
class SupplierAvailability:
    supplier: Supplier
    solution_type: SolutionType
    cost_per_kwh: float
