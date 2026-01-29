#!/usr/bin/env python
"""
CLI placeholder for downloading KITTI or nuScenes datasets.
Implements structure only; actual download logic to be added with credentials/links.
"""
from pathlib import Path
import argparse

from app.pipeline.dataset_loader import DatasetName, ensure_dataset_present


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download KITTI or nuScenes datasets")
    parser.add_argument("dataset", choices=["kitti", "nuscenes"], help="Dataset name")
    parser.add_argument("--target", default="data/raw", help="Target directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_dir = Path(args.target)
    ensure_dataset_present(args.dataset, target_dir / args.dataset)
    print(f"Dataset placeholder ensured at {target_dir.resolve()}")


if __name__ == "__main__":
    main()
