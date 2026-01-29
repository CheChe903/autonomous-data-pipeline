from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import json

from app.models.dto import BoundingBox


def parse_nuscenes_sample(sample_annotation: Dict) -> List[BoundingBox]:
    """
    Placeholder: nuScenes JSON contains box coordinates in 3D; for 2D projection
    this would require camera intrinsics. Here we leave a stub to be filled later.
    추후 카메라 내·외부 파라미터로 3D→2D 투영을 구현해야 한다.
    """
    # TODO: implement 3D->2D box projection using calibrated sensor data.
    return []


def load_nuscenes_annotations(annotations_path: Path) -> Dict:
    # nuScenes annotation JSON 로드 헬퍼
    with annotations_path.open("r") as f:
        return json.load(f)
