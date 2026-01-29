from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from app.models.dto import BoundingBox


def parse_kitti_label_file(label_path: Path) -> List[BoundingBox]:
    """
    KITTI label format (per line):
    type truncation occlusion alpha bbox_left bbox_top bbox_right bbox_bottom ... (rest omitted)
    We parse class + bbox only.
    각 줄에서 클래스명과 2D 바운딩 박스 좌표만 추출한다.
    """
    boxes: List[BoundingBox] = []
    with label_path.open("r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            label = parts[0]
            x_min, y_min, x_max, y_max = map(float, parts[4:8])
            boxes.append(BoundingBox(label=label, x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max, attributes={}))
    return boxes


def iter_kitti_images(image_dir: Path, exts: Iterable[str] = (".png", ".jpg", ".jpeg")) -> Iterable[Path]:
    # 지정 폴더에서 이미지 확장자 목록을 순회
    for ext in exts:
        yield from image_dir.glob(f"*{ext}")
