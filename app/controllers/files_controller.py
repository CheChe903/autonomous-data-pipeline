from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.file import File
from app.schemas.upload import MediaType

router = APIRouter(prefix="/files", tags=["files"])


@router.get("")
def list_files(
    vehicle_id: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    route_id: Optional[str] = Query(None),
    media_type: Optional[MediaType] = Query(None),
    min_blur: Optional[float] = Query(None),
    captured_from: Optional[str] = Query(None),
    captured_to: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
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
    if min_blur is not None:
        filters.append(File.computed_json["blur_score"].as_float() >= min_blur)
    if captured_from:
        filters.append(File.captured_at >= datetime.fromisoformat(captured_from.replace("Z", "+00:00")))
    if captured_to:
        filters.append(File.captured_at <= datetime.fromisoformat(captured_to.replace("Z", "+00:00")))

    stmt = select(File).where(and_(*filters) if filters else True).offset(offset).limit(limit)
    return db.scalars(stmt).all()


@router.get("/{file_id}")
def get_file(file_id: str, db: Session = Depends(get_session)):
    obj = db.get(File, file_id)
    if not obj:
        raise HTTPException(status_code=404, detail="File not found")
    return obj
