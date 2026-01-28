from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Task Management API"
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return "sqlite:///./tasks.db"
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()