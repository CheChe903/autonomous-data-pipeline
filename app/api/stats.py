from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.schemas import StatsResponse
from app.models.orm import Image, Detection

router = APIRouter(prefix="/stats")


@router.get("", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_session)):
    total_images = db.scalar(select(func.count()).select_from(Image)) or 0
    total_detections = db.scalar(select(func.count()).select_from(Detection)) or 0

    label_rows = db.execute(select(Detection.label, func.count()).group_by(Detection.label)).all()
    label_histogram = {label: count for label, count in label_rows}

    blur_min, blur_avg, blur_max = db.execute(
        select(func.min(Image.quality_score), func.avg(Image.quality_score), func.max(Image.quality_score))
    ).one()
    blur_stats = {
        "min": float(blur_min) if blur_min is not None else 0.0,
        "avg": float(blur_avg) if blur_avg is not None else 0.0,
        "max": float(blur_max) if blur_max is not None else 0.0,
    }

    return StatsResponse(
        total_images=total_images,
        total_detections=total_detections,
        label_histogram=label_histogram,
        blur_stats=blur_stats,
    )
