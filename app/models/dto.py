from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class BoundingBox:
    # 하나의 객체 라벨과 2D 바운딩 박스 좌표를 표현
    label: str
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    attributes: Dict[str, Any] | None = None


@dataclass
class ImageRecord:
    # 전처리된 이미지 한 장과 관련 메타데이터 + 라벨 목록
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
