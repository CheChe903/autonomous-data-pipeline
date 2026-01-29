from typing import Tuple

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # storage
    storage_mode: str = Field("local", alias="STORAGE_MODE")  # local|minio
    storage_base_path: str = Field("./data", alias="STORAGE_BASE_PATH")
    minio_endpoint: str = Field("http://localhost:9000", alias="MINIO_ENDPOINT")
    minio_root_user: str = Field("minioadmin", alias="MINIO_ROOT_USER")
    minio_root_password: str = Field("minioadmin", alias="MINIO_ROOT_PASSWORD")
    minio_bucket: str = Field("autonomous-data", alias="MINIO_BUCKET")

    # preprocessing
    image_size: Tuple[int, int] = Field((640, 640), alias="IMAGE_SIZE")
    image_format: str = Field("jpeg", alias="IMAGE_FORMAT")  # jpeg|png
    jpeg_quality: int = Field(90, alias="JPEG_QUALITY")
    allow_png: bool = Field(True, alias="ALLOW_PNG")
    blur_threshold: float = Field(40.0, alias="BLUR_THRESHOLD")  # lenient initial threshold

    # datasets
    dataset_root: str = Field("./data/raw", alias="DATASET_ROOT")
    processed_root: str = Field("./data/processed", alias="PROCESSED_ROOT")
    dataset_preference: str = Field("kitti", alias="DATASET_PREFERENCE")  # kitti|nuscenes


settings = Settings()
