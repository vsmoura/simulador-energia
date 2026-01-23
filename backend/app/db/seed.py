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
        logo_url=(
            "data:image/png;base64,"
            "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"
            "o1Vt7Y/q/wP2CJOD+26F5QAAAABJRU5ErkJggg=="
        ),
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
