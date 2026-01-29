from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.settings import settings
from app.models.orm import Image, Detection

router = APIRouter(prefix="/download")


@router.get("/dataset")
def download_dataset(
    label: Optional[str] = Query(None, description="특정 라벨 포함 필터"),
    min_quality: Optional[float] = Query(None, description="블러 스코어 이상 필터"),
    db: Session = Depends(get_session),
):
    if settings.storage_mode != "local":
        raise HTTPException(status_code=501, detail="현재는 로컬 스토리지 ZIP만 지원")

    stmt = select(Image)
    if min_quality is not None:
        stmt = stmt.where(Image.quality_score >= min_quality)
    if label:
        stmt = stmt.join(Image.detections).where(Detection.label == label)
    images = db.scalars(stmt).all()
    if not images:
        raise HTTPException(status_code=404, detail="No images found for given filters")

    with tempfile.TemporaryDirectory() as tmpdir:
        bundle_dir = Path(tmpdir) / "bundle"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        for img in images:
            src = Path(img.processed_path)
            if not src.exists():
                continue
            shutil.copy2(src, bundle_dir / src.name)
        archive_path = shutil.make_archive(base_name=str(bundle_dir), format="zip", root_dir=bundle_dir)
        return FileResponse(archive_path, filename="dataset.zip")
