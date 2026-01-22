import strawberry

from app.domain.quotes import SolutionType

SolutionTypeEnum = strawberry.enum(SolutionType, name="SolutionType")

@strawberry.type
class SupplierQuoteType:
    supplier_id: int
    supplier_name: str
    supplier_logo_url: str
    supplier_origin_state: str
    total_customers: int
    average_rating: float
    solution_type: SolutionTypeEnum
    cost_per_kwh: float
    cost_total: float
    economy: float
    economy_percent: float


@strawberry.type
class SolutionQuoteType:
    solution_type: SolutionTypeEnum
    best_economy: float
    best_economy_percent: float
    suppliers: list[SupplierQuoteType]


@strawberry.type
class StateQuoteType:
    state_code: str
    state_name: str
    base_tariff_per_kwh: float
    consumption_kwh: float
    base_cost: float
    solutions: list[SolutionQuoteType]


@strawberry.type
class StateType:
    code: str
    name: str
    base_tariff_per_kwh: float
