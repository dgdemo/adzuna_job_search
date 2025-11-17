from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    adzuna_app_id: str | None = None
    adzuna_app_key: str | None = None
    adzuna_base_url: str = "https://api.adzuna.com/v1/api/jobs"

    # Pydantic v2-style configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
