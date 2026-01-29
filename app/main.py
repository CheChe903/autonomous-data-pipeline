from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core import database
from app.controllers import health_controller, upload_controller, files_controller, stats_controller, download_controller


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
    # DB 테이블 생성 (개발용). 운영 시 Alembic 권장.
    database.Base.metadata.create_all(bind=database.engine)

    app.include_router(health_controller.router)
    app.include_router(upload_controller.router, prefix=settings.api_prefix)
    app.include_router(files_controller.router, prefix=settings.api_prefix)
    app.include_router(stats_controller.router, prefix=settings.api_prefix)
    app.include_router(download_controller.router, prefix=settings.api_prefix)
    return app


app = create_app()
