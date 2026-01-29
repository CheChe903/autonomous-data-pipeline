from __future__ import annotations

import shutil
import tempfile
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.file import File

router = APIRouter(prefix="/download", tags=["download"])


@router.get("/dataset")
def download_dataset(
    vehicle_id: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    route_id: Optional[str] = Query(None),
    media_type: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    filters = []
    if vehicle_id:
        filters.append(File.vehicle_id == vehicle_id)
    if source:
        filters.append(File.source == source)
    if route_id:
        filters.append(File.route_id == route_id)
    if media_type:
        filters.append(File.media_type == media_type)

    stmt = select(File).where(and_(*filters) if filters else True)
    files = db.scalars(stmt).all()
    if not files:
        raise HTTPException(status_code=404, detail="No files for given filters")

    with tempfile.TemporaryDirectory() as tmpdir:
        bundle_dir = Path(tmpdir) / "bundle"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            src = Path(f.processed_path)
            if src.exists():
                shutil.copy2(src, bundle_dir / src.name)
        archive_path = shutil.make_archive(str(bundle_dir), "zip", root_dir=bundle_dir)
        return FileResponse(archive_path, filename="dataset.zip")
