from __future__ import annotations

from typing import Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.core.database import get_session
from app.models import schemas
from app.models.orm import Image, Detection

router = APIRouter(prefix="/images")


@router.get("", response_model=List[schemas.ImageOut])
def list_images(
    label: Optional[str] = Query(None, description="특정 라벨을 포함한 이미지만"),
    min_quality: Optional[float] = Query(None, description="블러 스코어 이상 필터"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_session),
):
    stmt = select(Image).offset(offset).limit(limit)
    if min_quality is not None:
        stmt = stmt.where(Image.quality_score >= min_quality)
    if label:
        stmt = stmt.join(Image.detections).where(Detection.label == label)
    images = db.scalars(stmt).all()
    return images


@router.get("/{image_id}", response_model=schemas.ImageOut)
def get_image(image_id: int, db: Session = Depends(get_session)):
    image = db.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
