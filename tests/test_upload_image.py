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


def make_dummy_video(tmpdir: Path) -> Path:
    path = tmpdir / "test.avi"
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(str(path), fourcc, 10.0, (64, 48))
    frame = np.zeros((48, 64, 3), dtype=np.uint8)
    for _ in range(5):
        writer.write(frame)
    writer.release()
    return path


def base_meta():
    return {
        "vehicle_id": "car-001",
        "captured_at": "2025-01-01T10:00:00Z",
        "source": "camera_front",
        "route_id": "route-1",
    }


def test_upload_image(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("STORAGE_BASE_PATH", str(tmp_path / "data"))
    monkeypatch.setenv("META_PATH", str(tmp_path / "meta"))

    img_path = make_dummy_image(tmp_path)
    meta = base_meta()

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


def test_upload_video(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("STORAGE_BASE_PATH", str(tmp_path / "data"))
    monkeypatch.setenv("META_PATH", str(tmp_path / "meta"))

    video_path = make_dummy_video(tmp_path)
    meta = base_meta()

    client = TestClient(app)
    with video_path.open("rb") as f:
        resp = client.post(
            "/api/upload",
            files={"file": ("test.avi", f, "video/avi")},
            data={"metadata": json.dumps(meta)},
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["media_type"] == "video"
    assert body["computed"]["frame_count"] == 5
    assert Path(body["stored_path"]).exists()
    assert Path(body["processed_path"]).exists()


def test_upload_missing_meta_field(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("STORAGE_BASE_PATH", str(tmp_path / "data"))
    monkeypatch.setenv("META_PATH", str(tmp_path / "meta"))

    img_path = make_dummy_image(tmp_path)
    meta = {"vehicle_id": "car-001"}  # missing captured_at, source, route_id

    client = TestClient(app)
    with img_path.open("rb") as f:
        resp = client.post(
            "/api/upload",
            files={"file": ("test.jpg", f, "image/jpeg")},
            data={"metadata": json.dumps(meta)},
        )
    assert resp.status_code == 400
    assert "Missing metadata" in resp.text


def test_upload_unsupported_ext(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("STORAGE_BASE_PATH", str(tmp_path / "data"))
    monkeypatch.setenv("META_PATH", str(tmp_path / "meta"))

    bogus = tmp_path / "file.txt"
    bogus.write_text("hello")
    meta = base_meta()

    client = TestClient(app)
    with bogus.open("rb") as f:
        resp = client.post(
            "/api/upload",
            files={"file": ("file.txt", f, "text/plain")},
            data={"metadata": json.dumps(meta)},
        )
    assert resp.status_code == 400
    assert "Unsupported file extension" in resp.text
