from typing import Tuple

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # .env 값을 로드해 앱 전역 설정으로 사용
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # storage
    storage_mode: str = Field("local", alias="STORAGE_MODE")  # local|minio 사용 여부
    storage_base_path: str = Field("./data", alias="STORAGE_BASE_PATH")  # 로컬 저장 루트
    minio_endpoint: str = Field("http://localhost:9000", alias="MINIO_ENDPOINT")  # MinIO 엔드포인트
    minio_root_user: str = Field("minioadmin", alias="MINIO_ROOT_USER")
    minio_root_password: str = Field("minioadmin", alias="MINIO_ROOT_PASSWORD")
    minio_bucket: str = Field("autonomous-data", alias="MINIO_BUCKET")

    # preprocessing
    image_size: Tuple[int, int] = Field((640, 640), alias="IMAGE_SIZE")  # 기본 리사이즈 크기
    image_format: str = Field("jpeg", alias="IMAGE_FORMAT")  # jpeg|png 기본 저장 포맷
    jpeg_quality: int = Field(90, alias="JPEG_QUALITY")  # JPEG 품질 (0-100)
    allow_png: bool = Field(True, alias="ALLOW_PNG")  # PNG 저장 허용 여부
    blur_threshold: float = Field(40.0, alias="BLUR_THRESHOLD")  # 블러 필터 임계값(관대)

    # datasets
    dataset_root: str = Field("./data/raw", alias="DATASET_ROOT")  # 원본 데이터 루트
    processed_root: str = Field("./data/processed", alias="PROCESSED_ROOT")  # 전처리 결과 루트
    dataset_preference: str = Field("kitti", alias="DATASET_PREFERENCE")  # 우선 처리할 데이터셋


settings = Settings()
