from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext


@dataclass(frozen=True)
class GraphQLContext(BaseContext):
    db: Session
