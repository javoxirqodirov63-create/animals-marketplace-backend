from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import shutil
from pathlib import Path

from app.config import settings
router = APIRouter(prefix="/upload", tags=["Rasmlar yuklash (Image Upload)"])

UPLOAD_DIR = settings.UPLOAD_DIR

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

@router.post("", summary="Hayvon rasmini serverga yuklash")
async def upload_image(file: UploadFile = File(...)):
    """
    Kamera yoki galereyadan tanlangan rasmni serverga yuklaydi.
    Yuklangan rasm havolasini (URL) qaytaradi.
    """
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Faqat quyidagi rasm formatlari qabul qilinadi: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = UPLOAD_DIR / unique_name
    
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "success": True,
        "filename": unique_name,
        "url": f"http://127.0.0.1:8000/uploads/{unique_name}"
    }
