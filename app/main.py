from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.controllers import health_controller, upload_controller


def create_app() -> FastAPI:
    # FastAPI 앱 생성 및 라우터 구성
    app = FastAPI(title="Data Backend", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_controller.router)
    app.include_router(upload_controller.router, prefix=settings.api_prefix)
    return app


app = create_app()
