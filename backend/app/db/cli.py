from __future__ import annotations

import argparse

from alembic import command
from alembic.config import Config

from app.db.seed import seed_database
from app.db.session import SessionLocal


def _alembic_config() -> Config:
    return Config("alembic.ini")


def run_migrations() -> None:
    command.upgrade(_alembic_config(), "head")


def run_seed() -> None:
    session = SessionLocal()
    try:
        seed_database(session)
    finally:
        session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Database maintenance commands")
    parser.add_argument("command", choices={"migrate", "seed"})
    args = parser.parse_args()

    if args.command == "migrate":
        run_migrations()
    elif args.command == "seed":
        run_seed()


if __name__ == "__main__":
    main()
