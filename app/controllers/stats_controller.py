from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models.file import File

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def stats(db: Session = Depends(get_session)):
    total_files = db.scalar(select(func.count()).select_from(File)) or 0

    by_media = db.execute(select(File.media_type, func.count()).group_by(File.media_type)).all()
    media_hist = {m: c for m, c in by_media}

    blur_min, blur_avg, blur_max = db.execute(
        select(func.min(File.computed_json["blur_score"].as_float()),
               func.avg(File.computed_json["blur_score"].as_float()),
               func.max(File.computed_json["blur_score"].as_float()))
    ).one()
    blur_stats = {
        "min": float(blur_min) if blur_min is not None else 0.0,
        "avg": float(blur_avg) if blur_avg is not None else 0.0,
        "max": float(blur_max) if blur_max is not None else 0.0,
    }

    return {
        "total_files": total_files,
        "media_histogram": media_hist,
        "blur_stats": blur_stats,
    }
