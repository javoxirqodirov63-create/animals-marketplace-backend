import os
from pathlib import Path

# Asosiy papkalar
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = os.getenv("SQLITE_DB_PATH", str(BASE_DIR / "marketplace_demo.db"))

class Settings:
    PROJECT_NAME: str = "Universal Hayvonlar Bozori API"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DB_PATH: str = DB_FILE
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-hayvonlar-bozori-2026")
    
settings = Settings()
