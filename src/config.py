from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # Service
    translator_host: str = "0.0.0.0"
    translator_port: int = 8001
    debug: bool = True
    log_level: str = "INFO"

    # Cache
    cache_type: Literal["memory", "redis"] = "memory"
    cache_max_size: int = 1000
    cache_ttl_seconds: int = 3600
    redis_url: str = "redis://localhost:6379"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period_seconds: int = 60

    # Translation
    default_source_lang: str = "auto"
    default_target_lang: str = "en"
    google_translator_timeout: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()