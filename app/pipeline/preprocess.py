from pathlib import Path
from typing import Iterable, Tuple

import cv2
import numpy as np


def preprocess_image(
    input_path: Path,
    output_path: Path,
    size: Tuple[int, int] = (640, 640),
) -> Path:
    """
    Resize and normalize image; output is written to output_path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = cv2.imread(str(input_path))
    if image is None:
        raise ValueError(f"Failed to read image: {input_path}")
    resized = cv2.resize(image, size)
    normalized = resized.astype(np.float32) / 255.0
    # Store normalized image scaled back to 0-255 for visualization/storage
    cv2.imwrite(str(output_path), (normalized * 255).astype(np.uint8))
    return output_path


def batch_preprocess(inputs: Iterable[Path], output_root: Path, size: Tuple[int, int] = (640, 640)) -> Iterable[Path]:
    for path in inputs:
        rel = path.relative_to(path.parents[1]) if len(path.parents) > 1 else path.name
        yield preprocess_image(path, output_root / rel, size=size)
