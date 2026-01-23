from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from strawberry.fastapi import GraphQLRouter

from app.infrastructure.core.config import get_settings
from app.infrastructure.core.logging import configure_logging
from app.infrastructure.db.seed import seed_database
from app.infrastructure.db.session import get_db
from app.adapters.graphql.context import GraphQLContext
from app.adapters.graphql.schema import schema

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.api_version)

if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def get_context(db=Depends(get_db)) -> GraphQLContext:
    return GraphQLContext(db=db)


app.include_router(GraphQLRouter(schema, context_getter=get_context), prefix="/graphql")


@app.on_event("startup")
def startup_seed() -> None:
    for db in get_db():
        seed_database(db)
        break


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def db_health_check(db=Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
