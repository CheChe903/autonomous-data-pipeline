from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

import cv2

from app.core.config import settings
from app.models.dto import BoundingBox, ImageRecord
from app.parsers.kitti import iter_kitti_images, parse_kitti_label_file
from app.pipeline.preprocess import preprocess_image
from app.storage.adapter import get_storage


def kitti_paths(root: Path) -> Tuple[Path, Path]:
    """
    Returns (image_dir, label_dir) using common KITTI layout.
    Defaults to image_2/label_2 under root.
    """
    image_dir = root / "training" / "image_2"
    label_dir = root / "training" / "label_2"
    if not image_dir.exists() or not label_dir.exists():
        # fallback to direct children
        image_dir = root / "image_2"
        label_dir = root / "label_2"
    return image_dir, label_dir


def ingest_kitti(root: Path) -> List[ImageRecord]:
    image_dir, label_dir = kitti_paths(root)
    storage = get_storage()
    results: List[ImageRecord] = []

    for img_path in iter_kitti_images(image_dir):
        label_file = label_dir / f"{img_path.stem}.txt"
        annotations: List[BoundingBox] = []
        if label_file.exists():
            annotations = parse_kitti_label_file(label_file)

        # read metadata
        stat = img_path.stat()
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        height, width = img.shape[:2]

        processed_path, meta = preprocess_image(
            input_path=img_path,
            output_path=Path(settings.processed_root) / "kitti" / img_path.name,
            size=settings.image_size,
            image_format=settings.image_format,
            jpeg_quality=settings.jpeg_quality,
        )

        stored_original = storage.save(img_path, f"raw/kitti/{img_path.name}")
        stored_processed = storage.save(processed_path, f"processed/kitti/{processed_path.name}")

        record = ImageRecord(
            path=Path(stored_processed),
            width=meta["width"],
            height=meta["height"],
            size_bytes=stat.st_size,
            captured_at=None,
            weather=None,
            time_of_day=meta.get("time_of_day"),
            road_type=meta.get("road_type"),
            quality_score=meta.get("blur_score"),
            annotations=annotations,
        )
        results.append(record)
    return results
