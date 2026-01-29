from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Optional

from minio import Minio
from minio.error import S3Error

from app.core.config import settings


def get_minio_client() -> Minio:
    return Minio(
        settings.minio_endpoint.replace("http://", "").replace("https://", ""),
        access_key=settings.minio_root_user,
        secret_key=settings.minio_root_password,
        secure=settings.minio_endpoint.startswith("https"),
    )


def ensure_bucket(client: Minio, bucket: str) -> None:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


def upload_file(client: Minio, bucket: str, object_name: str, file_path: Path, content_type: Optional[str] = None) -> None:
    ensure_bucket(client, bucket)
    client.fput_object(bucket, object_name, str(file_path), content_type=content_type)


def upload_bytes(client: Minio, bucket: str, object_name: str, buffer: bytes, length: int, content_type: Optional[str] = None) -> None:
    ensure_bucket(client, bucket)
    data = BytesIO(buffer)
    client.put_object(bucket, object_name, data, length=length, content_type=content_type)


def download_file(client: Minio, bucket: str, object_name: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        client.fget_object(bucket, object_name, str(dest))
    except S3Error as exc:
        raise FileNotFoundError(object_name) from exc
    return dest
