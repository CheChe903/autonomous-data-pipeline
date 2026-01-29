import os

# 테스트에서는 로컬 sqlite DB를 사용해 외부 Postgres 의존성을 제거
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app.main import app

def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"
