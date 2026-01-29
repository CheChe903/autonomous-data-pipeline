from __future__ import annotations

import json
import tempfile
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.file import File
from app.schemas.upload import Metadata, UploadResponse, MediaType
from app.storage.local import LocalStorage
from app.utils.media import (
    detect_media_type,
    check_size,
    preprocess_image,
    extract_video_meta,
    sha256_file,
)


class UploadService:
    def __init__(self):
        self.storage = LocalStorage(Path(settings.storage_base_path))

    def _parse_metadata(self, metadata_str: str) -> Metadata:
        # 메타 JSON 파싱 및 필수 필드 검증
        try:
            raw = json.loads(metadata_str)
        except json.JSONDecodeError as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"Invalid metadata JSON: {exc}") from exc
        try:
            return Metadata(**raw)
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"Metadata validation failed: {exc}") from exc

    def _save_meta_file(self, record: dict) -> None:
        meta_dir = Path(settings.meta_path)
        meta_dir.mkdir(parents=True, exist_ok=True)
        (meta_dir / f"{record['id']}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))

    def process_upload(self, db: Session, file: UploadFile, metadata_str: str) -> UploadResponse:
        meta = self._parse_metadata(metadata_str)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / file.filename
            content = file.file.read()
            tmp_path.write_bytes(content)

            # 기본 검증 (크기/확장자)
            try:
                check_size(tmp_path, settings.max_file_size_mb)
                media_type: MediaType = detect_media_type(tmp_path, settings.allowed_image_exts, settings.allowed_video_exts)
            except ValueError as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

            file_id = uuid4().hex
            suffix = tmp_path.suffix.lower()

            # 전처리 / 메타 추출
            if media_type == "image":
                processed_path = self.storage.save(tmp_path, subdir="processed/images", suffix=".jpg")
                computed = preprocess_image(
                    src=tmp_path,
                    dst=processed_path,
                    resize=settings.image_resize,
                    jpeg_quality=settings.jpeg_quality,
                )
            else:
                processed_path = self.storage.save(tmp_path, subdir="processed/videos", suffix=suffix)
                computed = extract_video_meta(tmp_path)

            stored_path = self.storage.save(tmp_path, subdir="raw", suffix=suffix)
            file_hash = sha256_file(tmp_path)

        # DB 저장
        db_obj = File(
            id=file_id,
            original_filename=file.filename,
            stored_path=str(stored_path),
            processed_path=str(processed_path),
            media_type=media_type,
            size_bytes=len(content),
            sha256=file_hash,
            vehicle_id=meta.vehicle_id,
            captured_at=datetime.fromisoformat(meta.captured_at.replace("Z", "+00:00")),
            source=meta.source,
            route_id=meta.route_id,
            location_lat=meta.location_lat,
            location_lon=meta.location_lon,
            weather=meta.weather,
            note=meta.note,
            meta_json=meta.model_dump(),
            computed_json=computed,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        record = {
            "id": db_obj.id,
            "original_filename": db_obj.original_filename,
            "stored_path": db_obj.stored_path,
            "processed_path": db_obj.processed_path,
            "media_type": db_obj.media_type,
            "size_bytes": db_obj.size_bytes,
            "sha256": db_obj.sha256,
            "meta": db_obj.meta_json,
            "computed": db_obj.computed_json,
        }

        self._save_meta_file(record)
        return UploadResponse(**record)
