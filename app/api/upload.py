from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from app.core.settings import settings
from app.storage.local import LocalStorage
from app.utils.media import (
    detect_media_type,
    check_size,
    preprocess_image,
    extract_video_meta,
    sha256_file,
)

router = APIRouter(prefix="/upload", tags=["upload"])

RequiredMetaKeys = ["vehicle_id", "captured_at", "source", "route_id"]


@router.post("")
async def upload(
    file: UploadFile = File(..., description="이미지/동영상 파일"),
    metadata: str = Form(..., description="JSON 문자열 메타데이터"),
):
    # 1) 메타데이터 파싱/검증
    try:
        meta = json.loads(metadata)
    except json.JSONDecodeError as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Invalid metadata JSON: {exc}") from exc

    missing = [k for k in RequiredMetaKeys if k not in meta]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing metadata fields: {missing}")

    # 2) 파일 임시 저장
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / file.filename
        content = await file.read()
        tmp_path.write_bytes(content)

        # 3) 기본 검증 (크기/확장자)
        try:
            check_size(tmp_path, settings.max_file_size_mb)
            media_type = detect_media_type(tmp_path, settings.allowed_image_exts, settings.allowed_video_exts)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        # 4) 저장소 설정
        storage = LocalStorage(Path(settings.storage_base_path))

        file_id = uuid4().hex
        suffix = tmp_path.suffix.lower()

        # 5) 전처리/메타 추출 (이미지는 리사이즈·블러, 동영상은 메타만)
        computed = {}
        if media_type == "image":
            processed_path = storage.save(
                tmp_path,
                subdir="processed/images",
                suffix=".jpg",
            )
            computed = preprocess_image(
                src=tmp_path,
                dst=processed_path,
                resize=settings.image_resize,
                jpeg_quality=settings.jpeg_quality,
            )
        else:  # video
            processed_path = storage.save(tmp_path, subdir="processed/videos", suffix=suffix)
            computed = extract_video_meta(tmp_path)

        stored_path = storage.save(tmp_path, subdir="raw", suffix=suffix)
        file_hash = sha256_file(tmp_path)

    # 6) 응답/저장용 레코드 구성
    record = {
        "id": file_id,
        "original_filename": file.filename,
        "stored_path": str(stored_path),
        "processed_path": str(processed_path),
        "media_type": media_type,
        "size_bytes": len(content),
        "sha256": file_hash,
        "meta": meta,
        "computed": computed,
    }

    # 7) 메타 JSON 저장
    meta_dir = Path(settings.meta_path)
    meta_dir.mkdir(parents=True, exist_ok=True)
    (meta_dir / f"{file_id}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))

    return JSONResponse(record)
