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
        logo_url=(
            "data:image/png;base64,"
            "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"
            "o1Vt7Y/q/wP2CJOD+26F5QAAAABJRU5ErkJggg=="
        ),
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
