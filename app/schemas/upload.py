from __future__ import annotations

from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

MediaType = Literal["image", "video"]


class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow")
    # 업로드 필수 메타
    vehicle_id: str
    captured_at: str  # ISO8601 string
    source: str  # e.g., camera_front
    route_id: str
    # 선택 필드
    location_lat: float | None = None
    location_lon: float | None = None
    weather: str | None = None
    note: str | None = None


class UploadResponse(BaseModel):
    id: str
    original_filename: str
    stored_path: str
    processed_path: str
    media_type: MediaType
    size_bytes: int
    sha256: str
    meta: dict
    computed: dict
