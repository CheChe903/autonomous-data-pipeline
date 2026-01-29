from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional


def infer_time_of_day(dt: Optional[datetime]) -> Optional[str]:
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
    if not meta:
        return None
    return meta.get("weather")


def infer_road_type_from_path(path: Path) -> Optional[str]:
    parts = {p.lower() for p in path.parts}
    for key in ("highway", "urban", "residential", "city", "rural"):
        if key in parts:
            return key
    return None
