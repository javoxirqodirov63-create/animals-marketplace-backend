import os
import shutil
from pathlib import Path

# Asosiy papkalar
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Vercel yoki serverless muhitni tekshirish
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("NOW_REGION") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

if IS_VERCEL:
    TMP_DIR = Path("/tmp")
    DB_FILE = str(TMP_DIR / "marketplace_demo.db")
    # Asl SQLite bazani /tmp ga nusxalash (serverless da faqat /tmp ga yozish mumkin)
    SOURCE_DB = BASE_DIR / "marketplace_demo.db"
    if SOURCE_DB.exists() and not Path(DB_FILE).exists():
        try:
            shutil.copy2(SOURCE_DB, DB_FILE)
        except Exception as e:
            print(f"Baza nusxalashda xatolik: {e}")
    UPLOAD_DIR = TMP_DIR / "uploads"
else:
    DB_FILE = os.getenv("SQLITE_DB_PATH", str(BASE_DIR / "marketplace_demo.db"))
    UPLOAD_DIR = BASE_DIR / "uploads"

try:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

class Settings:
    PROJECT_NAME: str = "Universal Hayvonlar Bozori API"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DB_PATH: str = DB_FILE
    UPLOAD_DIR: Path = UPLOAD_DIR
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-hayvonlar-bozori-2026")
    
settings = Settings()
