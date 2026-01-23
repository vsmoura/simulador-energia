from __future__ import annotations

from typing import Iterable

from app.application.repositories import QuoteRepository
from app.domain.quotes import InvalidConsumptionError
from app.domain.quotes import SolutionQuote
from app.domain.quotes import SolutionType
from app.domain.quotes import StateNotFoundError
from app.domain.quotes import StateQuote
from app.domain.quotes import SupplierQuote
from app.infrastructure.db.models import SupplierAvailability


def _build_supplier_quotes(
    repo: QuoteRepository,
    availabilities: Iterable[SupplierAvailability],
    consumption_kwh: float,
) -> dict[SolutionType, list[SupplierQuote]]:
    quotes: dict[SolutionType, list[SupplierQuote]] = {}
    for availability in availabilities:
        cost_per_kwh = repo.get_solution_cost(availability)
        if cost_per_kwh is None:
            continue
        supplier = availability.supplier
        solution_type = repo.get_solution_type(availability)
        cost_total = consumption_kwh * cost_per_kwh
        quotes.setdefault(solution_type, []).append(
            SupplierQuote(
                supplier_id=supplier.id,
                supplier_name=supplier.name,
                supplier_logo_url=supplier.logo_url,
                supplier_origin_state=supplier.origin_state.code,
                total_customers=supplier.total_customers,
                average_rating=supplier.average_rating,
                solution_type=solution_type,
                cost_per_kwh=cost_per_kwh,
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


class QuoteService:
    def __init__(self, repo: QuoteRepository) -> None:
        self.repo = repo

    def build_state_quote(self, state_code: str, consumption_kwh: float) -> StateQuote:
        if consumption_kwh <= 0:
            raise InvalidConsumptionError("Consumption must be greater than zero.")

        state = self.repo.get_state_with_suppliers(state_code)
        if state is None:
            raise StateNotFoundError(f"State {state_code} not found.")

        base_cost = consumption_kwh * state.base_tariff_per_kwh
        availabilities = self.repo.get_supplier_availabilities(state)
        supplier_quotes = _build_supplier_quotes(self.repo, availabilities, consumption_kwh)
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
