from __future__ import annotations

import shutil
from pathlib import Path
from typing import Protocol

from app.core.settings import settings
from app.storage.minio_client import MinioClientWrapper


class Storage(Protocol):
    # src 파일을 목적지 키로 저장하고 최종 경로/URI를 반환
    def save(self, src: Path, dest_key: str) -> str:
        ...


class LocalStorage:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, src: Path, dest_key: str) -> str:
        # 로컬 디렉터리에 파일 복사
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
        # MinIO/S3에 업로드 후 s3:// 형태 URI 반환
        self.client.upload_file(bucket=self.bucket, object_name=dest_key, file_path=src)
        return f"s3://{self.bucket}/{dest_key}"


def get_storage() -> Storage:
    if settings.storage_mode == "minio":
        return MinioStorage(bucket=settings.minio_bucket)
    return LocalStorage(base_path=Path(settings.storage_base_path))
