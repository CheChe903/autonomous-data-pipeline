from __future__ import annotations

from pathlib import Path

from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class MinioClientWrapper:
    def __init__(self) -> None:
        endpoint = settings.minio_endpoint.replace("http://", "").replace("https://", "")
        self.client = Minio(
            endpoint,
            access_key=settings.minio_root_user,
            secret_key=settings.minio_root_password,
            secure=settings.minio_endpoint.startswith("https"),
        )

    def ensure_bucket(self, bucket: str) -> None:
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    def upload_file(self, bucket: str, object_name: str, file_path: Path) -> None:
        try:
            self.ensure_bucket(bucket)
            self.client.fput_object(bucket, object_name, str(file_path))
        except S3Error as exc:
            raise RuntimeError(f"MinIO upload failed: {exc}") from exc
