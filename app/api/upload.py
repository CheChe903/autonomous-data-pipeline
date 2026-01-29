from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.settings import settings
from app.models import schemas
from app.models.orm import Detection, Image
from app.parsers.kitti import parse_kitti_label_file
from app.pipeline.preprocess import preprocess_image
from app.storage.adapter import get_storage

router = APIRouter(prefix="/upload")


@router.post("", response_model=schemas.UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    label_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_session),
):
    # 1) 임시 저장 후 전처리
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_img_path = Path(tmpdir) / file.filename
        content = await file.read()
        tmp_img_path.write_bytes(content)

        # optional 라벨 파일 저장
        tmp_label_path = None
        if label_file is not None:
            tmp_label_path = Path(tmpdir) / label_file.filename
            tmp_label_path.write_bytes(await label_file.read())

        processed_path, meta = preprocess_image(
            input_path=tmp_img_path,
            output_path=Path(settings.processed_root) / "upload" / file.filename,
            size=settings.image_size,
            image_format=settings.image_format,
            jpeg_quality=settings.jpeg_quality,
        )

        storage = get_storage()
        stored_original = storage.save(tmp_img_path, f"raw/upload/{file.filename}")
        stored_processed = storage.save(processed_path, f"processed/upload/{processed_path.name}")

    # 2) 라벨 파싱(KITTI 포맷 가정)
    detections = []
    if tmp_label_path:
        try:
            detections = parse_kitti_label_file(tmp_label_path)
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail=f"Label parse error: {exc}") from exc

    # 3) DB 저장
    image_row = Image(
        original_path=str(stored_original),
        processed_path=str(stored_processed),
        width=meta["width"],
        height=meta["height"],
        size_bytes=len(content),
        captured_at=None,
        weather=None,
        time_of_day=meta.get("time_of_day"),
        road_type=meta.get("road_type"),
        quality_score=meta.get("blur_score"),
    )
    db.add(image_row)
    db.flush()

    for det in detections:
        det_row = Detection(
            image_id=image_row.id,
            object_id=None,
            label=det.label,
            confidence=None,
            x_min=det.x_min,
            y_min=det.y_min,
            x_max=det.x_max,
            y_max=det.y_max,
            attributes=None,
        )
        db.add(det_row)

    db.commit()
    db.refresh(image_row)
    return schemas.UploadResponse(image=image_row)
