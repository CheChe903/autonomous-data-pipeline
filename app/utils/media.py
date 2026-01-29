from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Tuple, Literal

import cv2
import numpy as np

MediaType = Literal["image", "video"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_media_type(path: Path, allowed_images: list[str], allowed_videos: list[str]) -> MediaType:
    ext = path.suffix.lower()
    if ext in allowed_images:
        return "image"
    if ext in allowed_videos:
        return "video"
    raise ValueError(f"Unsupported file extension: {ext}")


def check_size(path: Path, max_mb: int) -> None:
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > max_mb:
        raise ValueError(f"File too large: {size_mb:.1f}MB > {max_mb}MB")


def compute_blur_score(image: np.ndarray) -> float:
    return float(cv2.Laplacian(image, cv2.CV_64F).var())


def preprocess_image(
    src: Path,
    dst: Path,
    resize: Tuple[int, int],
    jpeg_quality: int,
) -> dict:
    img = cv2.imread(str(src))
    if img is None:
        raise ValueError("Invalid image data")
    resized = cv2.resize(img, resize)
    blur = compute_blur_score(resized)
    dst.parent.mkdir(parents=True, exist_ok=True)
    params = [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)] if dst.suffix.lower() in {".jpg", ".jpeg"} else []
    cv2.imwrite(str(dst), resized, params)
    return {
        "width": resized.shape[1],
        "height": resized.shape[0],
        "blur_score": blur,
    }


def extract_video_meta(src: Path) -> dict:
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise ValueError("Invalid video data")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0.0
    cap.release()
    return {
        "frame_count": frame_count,
        "fps": fps,
        "duration_sec": duration,
        "width": width,
        "height": height,
    }
