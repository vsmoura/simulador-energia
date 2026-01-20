from fastapi import Depends
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.core.config import get_settings
from app.db.seed import seed_database
from app.db.session import get_db
from app.graphql.context import GraphQLContext
from app.graphql.schema import schema

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.api_version)


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