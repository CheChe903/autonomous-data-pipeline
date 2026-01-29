from fastapi import FastAPI

from app.api import routes
from app.core.config import settings


def create_application() -> FastAPI:
    app = FastAPI(title="Autonomous Data Pipeline", version="0.1.0")
    app.include_router(routes.router, prefix=settings.api_prefix)
    return app


app = create_application()
