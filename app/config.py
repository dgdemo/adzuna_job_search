from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    adzuna_app_id: str | None = None
    adzuna_app_key: str | None = None
    adzuna_base_url: str = "https://api.adzuna.com/v1/api"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
