from typing import Tuple, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    api_prefix: str = Field("/api", alias="API_PREFIX")

    storage_base_path: str = Field("./data", alias="STORAGE_BASE_PATH")
    processed_path: str = Field("./data/processed", alias="PROCESSED_PATH")
    meta_path: str = Field("./data/meta", alias="META_PATH")

    allowed_image_exts: List[str] = Field(default_factory=lambda: [".jpg", ".jpeg", ".png", ".bmp"])
    allowed_video_exts: List[str] = Field(default_factory=lambda: [".mp4", ".mov", ".avi", ".mkv"])
    max_file_size_mb: int = Field(500, alias="MAX_FILE_SIZE_MB")  # 단일 업로드 허용 최대 크기

    image_resize: Tuple[int, int] = Field((640, 640), alias="IMAGE_RESIZE")
    jpeg_quality: int = Field(90, alias="JPEG_QUALITY")


settings = Settings()
