from pathlib import Path
from typing import Literal


DatasetName = Literal["kitti", "nuscenes"]


def ensure_dataset_present(dataset: DatasetName, target_dir: Path) -> Path:
    """
    Placeholder for dataset download/extract logic.
    Returns path where the dataset is stored.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    # TODO: implement KITTI/nuScenes authenticated download and checksum validation
    return target_dir
