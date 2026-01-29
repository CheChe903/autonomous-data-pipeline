from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class DetectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    label: str
    confidence: float | None = None
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    attributes: str | None = None


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    original_path: str
    processed_path: str
    width: int
    height: int
    size_bytes: int
    captured_at: Optional[datetime] = None
    weather: Optional[str] = None
    time_of_day: Optional[str] = None
    road_type: Optional[str] = None
    quality_score: Optional[float] = None
    detections: List[DetectionOut] = Field(default_factory=list)


class UploadResponse(BaseModel):
    image: ImageOut


class StatsResponse(BaseModel):
    total_images: int
    total_detections: int
    label_histogram: dict[str, int]
    blur_stats: dict[str, float]
