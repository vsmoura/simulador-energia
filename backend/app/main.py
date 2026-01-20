from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.core.config import get_settings
from app.graphql.schema import schema

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.api_version)

app.include_router(GraphQLRouter(schema), prefix="/graphql")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
