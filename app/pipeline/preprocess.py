from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

import cv2
import numpy as np

from app.pipeline.classifier import infer_road_type_from_path, infer_time_of_day


def compute_blur_score(image: np.ndarray) -> float:
    # 라플라시안 분산으로 선명도 측정(낮을수록 흐림)
    return float(cv2.Laplacian(image, cv2.CV_64F).var())


def preprocess_image(
    input_path: Path,
    output_path: Path,
    size: Tuple[int, int] = (640, 640),
    image_format: str = "jpeg",
    jpeg_quality: int = 90,
) -> tuple[Path, dict]:
    """
    이미지 리사이즈·정규화 후 지정 포맷으로 저장.
    반환: (저장 경로, 메타데이터 딕셔너리)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError(f"Failed to read image: {input_path}")
    resized = cv2.resize(image, size)
    normalized = resized.astype(np.float32) / 255.0
    blur_score = compute_blur_score(resized)

    # 포맷별 인코딩 파라미터 설정
    params = []
    if image_format.lower() == "jpeg":
        params = [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)]
        ext = ".jpg"
    else:
        ext = ".png"

    target_path = output_path.with_suffix(ext)
    cv2.imwrite(str(target_path), (normalized * 255).astype(np.uint8), params)

    metadata = {
        "width": resized.shape[1],
        "height": resized.shape[0],
        "blur_score": blur_score,
        "time_of_day": infer_time_of_day(None),
        "road_type": infer_road_type_from_path(input_path),
    }
    return target_path, metadata


def batch_preprocess(
    inputs: Iterable[Path],
    output_root: Path,
    size: Tuple[int, int],
    image_format: str,
    jpeg_quality: int,
) -> Iterable[tuple[Path, dict]]:
    for path in inputs:
        relative = path.name
        yield preprocess_image(
            input_path=path,
            output_path=output_root / relative,
            size=size,
            image_format=image_format,
            jpeg_quality=jpeg_quality,
        )
