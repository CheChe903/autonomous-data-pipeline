from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional


def infer_time_of_day(dt: Optional[datetime]) -> Optional[str]:
    # 캡처 시각을 아침/오후/저녁/밤으로 단순 분류
    if dt is None:
        return None
    hour = dt.hour
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "night"


def infer_weather_from_metadata(meta: dict | None) -> Optional[str]:
    # 외부 메타데이터에 weather 키가 있으면 그대로 사용
    if not meta:
        return None
    return meta.get("weather")


def infer_road_type_from_path(path: Path) -> Optional[str]:
    # 경로명에 포함된 키워드로 도로 유형을 추정
    parts = {p.lower() for p in path.parts}
    for key in ("highway", "urban", "residential", "city", "rural"):
        if key in parts:
            return key
    return None
