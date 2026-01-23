from __future__ import annotations

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.domain.quotes import SolutionType
from app.infrastructure.db.base import Base


class State(Base):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(2), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    base_tariff_per_kwh: Mapped[float] = mapped_column(Float)

    suppliers: Mapped[list[SupplierAvailability]] = relationship(back_populates="state")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    logo_url: Mapped[str] = mapped_column(String(255))
    origin_state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    total_customers: Mapped[int] = mapped_column(Integer)
    average_rating: Mapped[float] = mapped_column(Float)

    origin_state: Mapped[State] = relationship()
    solutions: Mapped[list[SupplierSolution]] = relationship(back_populates="supplier")
    availability: Mapped[list[SupplierAvailability]] = relationship(back_populates="supplier")


class SupplierSolution(Base):
    __tablename__ = "supplier_solutions"
    __table_args__ = (UniqueConstraint("supplier_id", "solution_type", name="uq_supplier_solution"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    solution_type: Mapped[SolutionType] = mapped_column(
        SQLEnum(SolutionType, name="solution_type"),
        index=True,
    )
    cost_per_kwh: Mapped[float] = mapped_column(Float)

    supplier: Mapped[Supplier] = relationship(back_populates="solutions")


class SupplierAvailability(Base):
    __tablename__ = "supplier_availability"
    __table_args__ = (
        UniqueConstraint("supplier_id", "state_id", "solution_type", name="uq_supplier_state_solution"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    solution_type: Mapped[SolutionType] = mapped_column(
        SQLEnum(SolutionType, name="solution_type"),
        index=True,
    )

    supplier: Mapped[Supplier] = relationship(back_populates="availability")
    state: Mapped[State] = relationship(back_populates="suppliers")
