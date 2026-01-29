from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    api_prefix: str = Field("/api", alias="API_PREFIX")

    postgres_user: str = Field("adp", alias="POSTGRES_USER")
    postgres_password: str = Field("adp", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field("adp", alias="POSTGRES_DB")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    minio_endpoint: str = Field("http://localhost:9000", alias="MINIO_ENDPOINT")
    minio_root_user: str = Field("minioadmin", alias="MINIO_ROOT_USER")
    minio_root_password: str = Field("minioadmin", alias="MINIO_ROOT_PASSWORD")
    minio_bucket: str = Field("autonomous-data", alias="MINIO_BUCKET")

    storage_base_path: str = Field("./data", alias="STORAGE_BASE_PATH")

    yolo_model: str = Field("yolov8n.pt", alias="YOLO_MODEL")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
