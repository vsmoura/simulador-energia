from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SolutionType(str, Enum):
    GD = "GD"
    MERCADO_LIVRE = "MERCADO_LIVRE"


@dataclass(frozen=True)
class SupplierQuote:
    supplier_id: int
    supplier_name: str
    supplier_logo_url: str
    supplier_origin_state: str
    total_customers: int
    average_rating: float
    solution_type: SolutionType
    cost_per_kwh: float
    cost_total: float
    economy: float
    economy_percent: float


@dataclass(frozen=True)
class SolutionQuote:
    solution_type: SolutionType
    best_economy: float
    best_economy_percent: float
    suppliers: tuple[SupplierQuote, ...]


@dataclass(frozen=True)
class StateQuote:
    state_code: str
    state_name: str
    base_tariff_per_kwh: float
    consumption_kwh: float
    base_cost: float
    solutions: tuple[SolutionQuote, ...]


class StateNotFoundError(ValueError):
    """Raised when the requested state is not available."""


class InvalidConsumptionError(ValueError):
    """Raised when the consumption is invalid."""
