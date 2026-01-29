#!/usr/bin/env python3
from pathlib import Path
import argparse

from app.pipeline.ingest import ingest_kitti
from app.core.config import settings


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest KITTI dataset (images + labels) into storage and DTO list.")
    parser.add_argument("--root", default=settings.dataset_root, help="KITTI dataset root (containing image_2/label_2)")
    return parser.parse_args()


def main():
    args = parse_args()
    records = ingest_kitti(Path(args.root))
    print(f"Ingested {len(records)} images (processed root: {settings.processed_root})")


if __name__ == "__main__":
    main()
