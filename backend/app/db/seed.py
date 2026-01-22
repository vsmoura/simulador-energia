from sqlalchemy.orm import Session

from app.domain.quotes import SolutionType
from app.infrastructure.db.models import State
from app.infrastructure.db.models import Supplier
from app.infrastructure.db.models import SupplierAvailability
from app.infrastructure.db.models import SupplierSolution
from app.domain.models import SolutionType
from app.domain.models import State
from app.domain.models import Supplier
from app.domain.models import SupplierAvailability
from app.domain.models import SupplierSolution


def seed_database(session: Session) -> None:
    if session.query(State).first():
        return

    states = [
        State(code="AC", name="Acre", base_tariff_per_kwh=0.88),
        State(code="AL", name="Alagoas", base_tariff_per_kwh=0.86),
        State(code="AP", name="Amapá", base_tariff_per_kwh=0.85),
        State(code="AM", name="Amazonas", base_tariff_per_kwh=0.84),
        State(code="BA", name="Bahia", base_tariff_per_kwh=0.82),
        State(code="CE", name="Ceará", base_tariff_per_kwh=0.72),
        State(code="DF", name="Distrito Federal", base_tariff_per_kwh=0.74),
        State(code="ES", name="Espírito Santo", base_tariff_per_kwh=0.70),
        State(code="GO", name="Goiás", base_tariff_per_kwh=0.75),
        State(code="MA", name="Maranhão", base_tariff_per_kwh=0.71),
        State(code="MT", name="Mato Grosso", base_tariff_per_kwh=0.85),
        State(code="MS", name="Mato Grosso do Sul", base_tariff_per_kwh=0.87),
        State(code="MG", name="Minas Gerais", base_tariff_per_kwh=0.80),
        State(code="PA", name="Pará", base_tariff_per_kwh=0.93),
        State(code="PB", name="Paraíba", base_tariff_per_kwh=0.66),
        State(code="PR", name="Paraná", base_tariff_per_kwh=0.63),
        State(code="PE", name="Pernambuco", base_tariff_per_kwh=0.74),
        State(code="PI", name="Piauí", base_tariff_per_kwh=0.83),
        State(code="RJ", name="Rio de Janeiro", base_tariff_per_kwh=0.87),
        State(code="RN", name="Rio Grande do Norte", base_tariff_per_kwh=0.72),
        State(code="RS", name="Rio Grande do Sul", base_tariff_per_kwh=0.70),
        State(code="RO", name="Rondônia", base_tariff_per_kwh=0.73),
        State(code="RR", name="Roraima", base_tariff_per_kwh=0.66),
        State(code="SC", name="Santa Catarina", base_tariff_per_kwh=0.62),
        State(code="SE", name="Sergipe", base_tariff_per_kwh=0.67),
        State(code="SP", name="São Paulo", base_tariff_per_kwh=0.67),
        State(code="TO", name="Tocantins", base_tariff_per_kwh=0.82),
    ]
    session.add_all(states)
    session.flush()
    states_by_code = {s.code: s for s in states}

    supplier_solatio = Supplier(
        name="Solatio Energia",
        logo_url="https://placehold.co/120x60?text=SOLATIO",
        origin_state_id=states_by_code["RN"].id,
        total_customers=18000,
        average_rating=4.5,
    )
    supplier_serena = Supplier(
        name="Serena Energia",
        logo_url="https://placehold.co/120x60?text=SERENA",
        origin_state_id=states_by_code["SP"].id,
        total_customers=9000,
        average_rating=4.4,
    )
    supplier_electy = Supplier(
        name="Electy Energia",
        logo_url="https://placehold.co/120x60?text=ELECTY",
        origin_state_id=states_by_code["SP"].id,
        total_customers=32000,
        average_rating=4.6,
    )
    supplier_engie = Supplier(
        name="Engie Brasil Energia",
        logo_url="https://placehold.co/120x60?text=ENGIE",
        origin_state_id=states_by_code["SC"].id,
        total_customers=1500,
        average_rating=4.6,
    )
    supplier_eneva = Supplier(
        name="Eneva",
        logo_url="https://placehold.co/120x60?text=ENEVA",
        origin_state_id=states_by_code["RJ"].id,
        total_customers=1100,
        average_rating=4.3,
    )
    supplier_matrix = Supplier(
        name="Matrix Energia",
        logo_url="https://placehold.co/120x60?text=MATRIX",
        origin_state_id=states_by_code["SP"].id,
        total_customers=3800,
        average_rating=4.5,
    )
    supplier_cpfl = Supplier(
        name="CPFL Energia",
        logo_url="https://placehold.co/120x60?text=CPFL",
        origin_state_id=states_by_code["SP"].id,
        total_customers=20000,
        average_rating=4.2,
    )
    supplier_aes = Supplier(
        name="AES Brasil",
        logo_url="https://placehold.co/120x60?text=AES",
        origin_state_id=states_by_code["SP"].id,
        total_customers=4200,
        average_rating=4.5,
    )
    supplier_noenergia = Supplier(
        name="Neoenergia",
        logo_url="https://placehold.co/120x60?text=NEO",
        origin_state_id=states_by_code["BA"].id,
        total_customers=14000,
        average_rating=4.1,
    )
    session.add_all(
        [supplier_solatio, 
         supplier_serena, 
         supplier_electy, 
         supplier_engie,
         supplier_eneva,
         supplier_matrix,
         supplier_cpfl,
         supplier_aes,
         supplier_noenergia,        
        ]
    )
    session.flush()

    session.add_all(
        [
            SupplierSolution(
                supplier_id=supplier_solatio.id,
                solution_type=SolutionType.GD,
                cost_per_kwh=0.39,
            ),
            SupplierSolution(
                supplier_id=supplier_electy.id,
                solution_type=SolutionType.GD,
                cost_per_kwh=0.36,
            ),
            SupplierSolution(
                supplier_id=supplier_noenergia.id,
                solution_type=SolutionType.GD,
                cost_per_kwh=0.41,
            ),
            SupplierSolution(
                supplier_id=supplier_cpfl.id,
                solution_type=SolutionType.GD,
                cost_per_kwh=0.43,
            ),
            SupplierSolution(
                supplier_id=supplier_matrix.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.49,
            ),
            SupplierSolution(
                supplier_id=supplier_engie.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.45,
            ),
            SupplierSolution(
                supplier_id=supplier_aes.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.47,
            ),
            SupplierSolution(
                supplier_id=supplier_serena.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.46,
            ),
            SupplierSolution(
                supplier_id=supplier_eneva.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.52,
            ),
            SupplierSolution(
                supplier_id=supplier_noenergia.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.50,
            ),
            SupplierSolution(
                supplier_id=supplier_cpfl.id,
                solution_type=SolutionType.MERCADO_LIVRE,
                cost_per_kwh=0.51,
            ),
        ]
    )
    session.flush()

    session.add_all(
        [
            # Matrix Energia (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_matrix.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # Engie (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_engie.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # AES (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_aes.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # Serena (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_serena.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # Eneva (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_eneva.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # Neoenergia (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_noenergia.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # CPFL (ACL)
            *[
                SupplierAvailability(
                    supplier_id=supplier_cpfl.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.MERCADO_LIVRE,
                )
                for uf in [
                    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA",
                    "PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SE","SP","TO"
                ]
            ],

            # Solatio
            *[
                SupplierAvailability(
                    supplier_id=supplier_solatio.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.GD,
                )
                for uf in ["RN","CE","PI","PE","BA","SE","MA","PB"]
            ],

            # Electy
            *[
                SupplierAvailability(
                    supplier_id=supplier_electy.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.GD,
                )
                for uf in ["SP","MG","RJ","ES","DF","GO","MS","MT","PR","SC","RS"]
            ],

            # Neoenergia
            *[
                SupplierAvailability(
                    supplier_id=supplier_noenergia.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.GD,
                )
                for uf in ["BA","PE","RN","DF","CE","SE","PB"]
            ],

            # CPFL
            *[
                SupplierAvailability(
                    supplier_id=supplier_cpfl.id,
                    state_id=states_by_code[uf].id,
                    solution_type=SolutionType.GD,
                )
                for uf in ["SP","MG","PR","SC","RS"]
            ],
        ]
    )   
    session.commit()
