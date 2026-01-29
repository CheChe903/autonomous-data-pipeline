from __future__ import annotations

import shutil
from pathlib import Path
from typing import Protocol

from app.core.config import settings
from app.storage.minio_client import MinioClientWrapper


class Storage(Protocol):
    def save(self, src: Path, dest_key: str) -> str:
        ...


class LocalStorage:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, src: Path, dest_key: str) -> str:
        target = self.base_path / dest_key
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        return str(target)


class MinioStorage:
    def __init__(self, bucket: str):
        self.client = MinioClientWrapper()
        self.bucket = bucket
        self.client.ensure_bucket(bucket)

    def save(self, src: Path, dest_key: str) -> str:
        self.client.upload_file(bucket=self.bucket, object_name=dest_key, file_path=src)
        return f"s3://{self.bucket}/{dest_key}"


def get_storage() -> Storage:
    if settings.storage_mode == "minio":
        return MinioStorage(bucket=settings.minio_bucket)
    return LocalStorage(base_path=Path(settings.storage_base_path))
