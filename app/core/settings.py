from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Tuple

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # API
    api_prefix: str = Field("/api", alias="API_PREFIX")

    # DB (postgres 우선)
    postgres_user: str = Field("adp", alias="POSTGRES_USER")
    postgres_password: str = Field("adp", alias="POSTGRES_PASSWORD")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_db: str = Field("adp", alias="POSTGRES_DB")

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
    blur_threshold: float = Field(40.0, alias="BLUR_THRESHOLD")

    # datasets
    dataset_root: str = Field("./data/raw", alias="DATASET_ROOT")
    processed_root: str = Field("./data/processed", alias="PROCESSED_ROOT")
    dataset_preference: str = Field("kitti", alias="DATASET_PREFERENCE")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
