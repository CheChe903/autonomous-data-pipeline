from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class BoundingBox:
    label: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    attributes: Dict[str, Any] | None = None


@dataclass
class ImageRecord:
    path: Path
    width: int
    height: int
    size_bytes: int
    captured_at: Optional[datetime]
    weather: Optional[str]
    time_of_day: Optional[str]
    road_type: Optional[str]
    quality_score: Optional[float]
    annotations: List[BoundingBox]
