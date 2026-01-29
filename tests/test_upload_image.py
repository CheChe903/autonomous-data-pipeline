import json
from pathlib import Path

import numpy as np
import cv2
from fastapi.testclient import TestClient

from app.main import app


def make_dummy_image(tmpdir: Path) -> Path:
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    cv2.rectangle(img, (20, 20), (180, 80), (255, 255, 255), 2)
    p = tmpdir / "test.jpg"
    cv2.imwrite(str(p), img)
    return p


def test_upload_image(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("STORAGE_BASE_PATH", str(tmp_path / "data"))
    monkeypatch.setenv("META_PATH", str(tmp_path / "meta"))

    img_path = make_dummy_image(tmp_path)
    meta = {
        "vehicle_id": "car-001",
        "captured_at": "2025-01-01T10:00:00Z",
        "source": "camera_front",
        "route_id": "route-1",
    }

    client = TestClient(app)
    with img_path.open("rb") as f:
        resp = client.post(
            "/api/upload",
            files={"file": ("test.jpg", f, "image/jpeg")},
            data={"metadata": json.dumps(meta)},
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["media_type"] == "image"
    assert "blur_score" in body["computed"]
    assert Path(body["stored_path"]).exists()
    assert Path(body["processed_path"]).exists()
