"""create initial tables

Revision ID: 001_create_tables
Revises: 
Create Date: 2024-10-01 00:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "001_create_tables"
down_revision = None
branch_labels = None
depends_on = None


solution_type_enum = sa.Enum("GD", "MERCADO_LIVRE", name="solution_type")


def upgrade() -> None:
    op.create_table(
        "states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=2), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("base_tariff_per_kwh", sa.Float(), nullable=False),
    )
    op.create_index(op.f("ix_states_code"), "states", ["code"], unique=True)

    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("logo_url", sa.String(length=255), nullable=False),
        sa.Column("origin_state_id", sa.Integer(), sa.ForeignKey("states.id"), nullable=False),
        sa.Column("total_customers", sa.Integer(), nullable=False),
        sa.Column("average_rating", sa.Float(), nullable=False),
    )
    op.create_index(op.f("ix_suppliers_name"), "suppliers", ["name"], unique=False)

    op.create_table(
        "supplier_solutions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("solution_type", solution_type_enum, nullable=False),
        sa.Column("cost_per_kwh", sa.Float(), nullable=False),
        sa.UniqueConstraint("supplier_id", "solution_type", name="uq_supplier_solution"),
    )
    op.create_index(op.f("ix_supplier_solutions_solution_type"), "supplier_solutions", ["solution_type"])

    op.create_table(
        "supplier_availability",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("state_id", sa.Integer(), sa.ForeignKey("states.id"), nullable=False),
        sa.Column("solution_type", solution_type_enum, nullable=False),
        sa.UniqueConstraint("supplier_id", "state_id", "solution_type", name="uq_supplier_state_solution"),
    )
    op.create_index(op.f("ix_supplier_availability_solution_type"), "supplier_availability", ["solution_type"])



def downgrade() -> None:
    op.drop_index(op.f("ix_supplier_availability_solution_type"), table_name="supplier_availability")
    op.drop_table("supplier_availability")

    op.drop_index(op.f("ix_supplier_solutions_solution_type"), table_name="supplier_solutions")
    op.drop_table("supplier_solutions")

    op.drop_index(op.f("ix_suppliers_name"), table_name="suppliers")
    op.drop_table("suppliers")

    op.drop_index(op.f("ix_states_code"), table_name="states")
    op.drop_table("states")

    solution_type_enum.drop(op.get_bind(), checkfirst=True)
