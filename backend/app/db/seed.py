from sqlalchemy.orm import Session

from app.domain.quotes import SolutionType
from app.infrastructure.db.models import State
from app.infrastructure.db.models import Supplier
from app.infrastructure.db.models import SupplierAvailability
from app.infrastructure.db.models import SupplierSolution


def seed_database(session: Session) -> None:
    if session.query(State).first():
        return

    states = [
        State(code="SP", name="São Paulo", base_tariff_per_kwh=0.62),
        State(code="RJ", name="Rio de Janeiro", base_tariff_per_kwh=0.68),
        State(code="MG", name="Minas Gerais", base_tariff_per_kwh=0.58),
    ]
    session.add_all(states)
    session.flush()

    supplier_alpha = Supplier(
        name="Energia Alfa",
        logo_url="https://placehold.co/120x60/png?text=Alfa",
        origin_state_id=states[0].id,
        total_customers=12000,
        average_rating=4.6,
    )
    supplier_beta = Supplier(
        name="Beta Power",
        logo_url="https://placehold.co/120x60/png?text=Beta",
        origin_state_id=states[1].id,
        total_customers=8000,
        average_rating=4.2,
    )
    supplier_gamma = Supplier(
        name="Gamma Energia",
        logo_url="https://placehold.co/120x60/png?text=Gamma",
        origin_state_id=states[2].id,
        total_customers=5300,
        average_rating=4.8,
    )

    session.add_all([supplier_alpha, supplier_beta, supplier_gamma])
    session.flush()

    session.add_all(
        [
            SupplierSolution(
                supplier_id=supplier_alpha.id,
                solution_type=SolutionType.GD,
                cost_per_kwh=0.51,
            ),
            SupplierSolution(
                supplier_id=supplier_alpha.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.47,
            ),
            SupplierSolution(
                supplier_id=supplier_beta.id,
                solution_type=SolutionType.GD,
                cost_per_kwh=0.53,
            ),
            SupplierSolution(
                supplier_id=supplier_gamma.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.44,
            ),
        ]
    )
    session.flush()

    session.add_all(
        [
            SupplierAvailability(
                supplier_id=supplier_alpha.id,
                state_id=states[0].id,
                solution_type=SolutionType.GD,
            ),
            SupplierAvailability(
                supplier_id=supplier_alpha.id,
                state_id=states[0].id,
                solution_type=SolutionType.MERCADO_LIVRE,
            ),
            SupplierAvailability(
                supplier_id=supplier_alpha.id,
                state_id=states[1].id,
                solution_type=SolutionType.GD,
            ),
            SupplierAvailability(
                supplier_id=supplier_beta.id,
                state_id=states[1].id,
                solution_type=SolutionType.GD,
            ),
            SupplierAvailability(
                supplier_id=supplier_beta.id,
                state_id=states[2].id,
                solution_type=SolutionType.GD,
            ),
            SupplierAvailability(
                supplier_id=supplier_gamma.id,
                state_id=states[0].id,
                solution_type=SolutionType.MERCADO_LIVRE,
            ),
            SupplierAvailability(
                supplier_id=supplier_gamma.id,
                state_id=states[2].id,
                solution_type=SolutionType.MERCADO_LIVRE,
            ),
        ]
    )

    session.commit()
