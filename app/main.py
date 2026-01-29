from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.settings import settings
from app.core.database import Base, engine

# DB 테이블 생성 (간단히 create_all 사용; 추후 Alembic으로 교체 가능)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Autonomous Data Pipeline API", version="0.1.0")

# CORS 기본 허용 (필요 시 제한)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix=settings.api_prefix)
