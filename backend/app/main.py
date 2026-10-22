from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.routers import locations, categories, auth, listings, chat, upload, admin, payments

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="""
# 🐾 Universal Hayvonlar Bozori (Animals-uz) REST API

Ushbu API uy hayvonlari, chorva mollari va parrandalar savdosi platformasi uchun ishlab chiqilgan.

### 🌟 Asosiy imkoniyatlar:
* **Autentifikatsiya:** Telefon raqam va SMS OTP orqali kirish
* **Hududlar:** O'zbekistonning 14 ta viloyati va barcha tumanlari
* **Kategoriyalar:** Chorva, Uy hayvonlari, Parrandalar va ularning osttoifalari
* **E'lonlar:** VIP/TOP e'lonlar, ko'rishlar va sevimlilar, filtrlash
* **Rasmlar:** Kamera va galereyadan fotosuratlarni yuklash (/api/upload)
* **Ichki Chat:** Real-time yozishmalar va xabarlar tarixi
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS sozlamalari (Flutter ilovasi yoki veb-sayt har qanday portdan so'rov yuborishi uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads statik papkasini ulash
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Routerlarni ulash
app.include_router(locations.router, prefix=settings.API_PREFIX)
app.include_router(categories.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(listings.router, prefix=settings.API_PREFIX)
app.include_router(chat.router, prefix=settings.API_PREFIX)
app.include_router(upload.router, prefix=settings.API_PREFIX)
app.include_router(payments.router, prefix=settings.API_PREFIX)
app.include_router(admin.router)

@app.get("/", summary="Tizim holati (Healthcheck)")
def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "documentation": "/docs",
        "message": "Universal Hayvonlar Bozori Backend API muvaffaqiyatli ishlamoqda!"
    }
