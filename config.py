import os
from dataclasses import dataclass

@dataclass
class Settings:
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    memory_db_path: str = os.getenv("MEMORY_DB_PATH", "data/clara_memory.db")
    alert_threshold: str = os.getenv("ALERT_THRESHOLD", "high")

settings = Settings()
