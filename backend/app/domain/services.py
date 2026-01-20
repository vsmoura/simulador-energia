from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.domain.models import SolutionType
from app.domain.models import State
from app.domain.models import Supplier
from app.domain.models import SupplierAvailability


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



def _build_supplier_quotes(
    availabilities: Iterable[SupplierAvailability],
    consumption_kwh: float,
) -> dict[SolutionType, list[SupplierQuote]]:
    quotes: dict[SolutionType, list[SupplierQuote]] = {}
    for availability in availabilities:
        supplier = availability.supplier
        solution = next(
            (solution for solution in supplier.solutions if solution.solution_type == availability.solution_type),
            None,
        )
        if solution is None:
            continue
        cost_total = consumption_kwh * solution.cost_per_kwh
        quotes.setdefault(availability.solution_type, []).append(
            SupplierQuote(
                supplier_id=supplier.id,
                supplier_name=supplier.name,
                supplier_logo_url=supplier.logo_url,
                supplier_origin_state=supplier.origin_state.code,
                total_customers=supplier.total_customers,
                average_rating=supplier.average_rating,
                solution_type=availability.solution_type,
                cost_per_kwh=solution.cost_per_kwh,
                cost_total=cost_total,
                economy=0.0,
                economy_percent=0.0,
            )
        )
    return quotes



def _apply_economy(
    quotes: dict[SolutionType, list[SupplierQuote]],
    base_cost: float,
) -> dict[SolutionType, list[SupplierQuote]]:
    updated: dict[SolutionType, list[SupplierQuote]] = {}
    for solution_type, supplier_quotes in quotes.items():
        enriched = []
        for quote in supplier_quotes:
            economy = base_cost - quote.cost_total
            economy_percent = (economy / base_cost) if base_cost else 0.0
            enriched.append(
                SupplierQuote(
                    supplier_id=quote.supplier_id,
                    supplier_name=quote.supplier_name,
                    supplier_logo_url=quote.supplier_logo_url,
                    supplier_origin_state=quote.supplier_origin_state,
                    total_customers=quote.total_customers,
                    average_rating=quote.average_rating,
                    solution_type=quote.solution_type,
                    cost_per_kwh=quote.cost_per_kwh,
                    cost_total=quote.cost_total,
                    economy=economy,
                    economy_percent=economy_percent,
                )
            )
        updated[solution_type] = enriched
    return updated



def build_state_quote(session: Session, state_code: str, consumption_kwh: float) -> StateQuote:
    if consumption_kwh <= 0:
        raise InvalidConsumptionError("Consumption must be greater than zero.")

    state = (
        session.query(State)
        .options(
            selectinload(State.suppliers)
            .selectinload(SupplierAvailability.supplier)
            .selectinload(Supplier.solutions)
        )
        .filter(State.code == state_code)
        .one_or_none()
    )
    if state is None:
        raise StateNotFoundError(f"State {state_code} not found.")

    base_cost = consumption_kwh * state.base_tariff_per_kwh
    supplier_quotes = _build_supplier_quotes(state.suppliers, consumption_kwh)
    supplier_quotes = _apply_economy(supplier_quotes, base_cost)

    solution_quotes: list[SolutionQuote] = []
    for solution_type, quotes in supplier_quotes.items():
        best_economy = max((quote.economy for quote in quotes), default=0.0)
        best_economy_percent = max((quote.economy_percent for quote in quotes), default=0.0)
        solution_quotes.append(
            SolutionQuote(
                solution_type=solution_type,
                best_economy=best_economy,
                best_economy_percent=best_economy_percent,
                suppliers=tuple(sorted(quotes, key=lambda item: item.economy, reverse=True)),
            )
        )

    return StateQuote(
        state_code=state.code,
        state_name=state.name,
        base_tariff_per_kwh=state.base_tariff_per_kwh,
        consumption_kwh=consumption_kwh,
        base_cost=base_cost,
        solutions=tuple(sorted(solution_quotes, key=lambda item: item.solution_type.value)),
    )
