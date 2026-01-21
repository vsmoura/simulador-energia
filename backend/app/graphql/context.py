from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session
from strawberry.fastapi import BaseContext


@dataclass
class GraphQLContext(BaseContext):
    db: Session
