from fastapi import APIRouter, HTTPException
import uuid
from typing import List
from app.database import get_db
from app.schemas.auth import SendOTPRequest, SendOTPResponse, VerifyOTPRequest, AuthTokenResponse, UserProfile

router = APIRouter(prefix="/auth", tags=["Autentifikatsiya (SMS OTP)"])

@router.post("/send-otp", response_model=SendOTPResponse, summary="SMS tasdiqlash kodini yuborish")
def send_otp(body: SendOTPRequest):
    """
    Foydalanuvchining telefon raqamiga 4 xonali SMS kod yuboradi.
    (Hozirgi test rejimida kod: '7777').
    """
    phone = body.phone_number.strip()
    if len(phone) < 9:
        raise HTTPException(status_code=400, detail="Telefon raqam noto'g'ri kiritildi")
    
    # Kelajakda Eskiz.uz / PlayMobile integratsiyasi shu yerga ulanadi
    return SendOTPResponse(
        success=True,
        message=f"{phone} raqamiga tasdiqlash kodi yuborildi",
        demo_code="7777"
    )

@router.post("/verify-otp", response_model=AuthTokenResponse, summary="SMS kodni tekshirish va tizimga kirish")
def verify_otp(body: VerifyOTPRequest):
    """
    SMS kodni tasdiqlaydi. Agar foydalanuvchi yangi bo'lsa, uni avtomatik ro'yxatdan o'tkazadi.
    """
    if body.code != "7777":
        raise HTTPException(status_code=400, detail="Tasdiqlash kodi noto'g'ri!")
    
    phone = body.phone_number.strip()
    
    with get_db() as db:
        db.execute("SELECT id, phone_number, full_name, avatar_url, role, is_verified FROM users WHERE phone_number = ?", (phone,))
        user = db.fetchone()
        
        if not user:
            # Yangi foydalanuvchi yaratish
            user_id = str(uuid.uuid4())
            name = body.full_name or "Yangi Foydalanuvchi"
            db.execute(
                "INSERT INTO users (id, phone_number, full_name, role, is_verified) VALUES (?, ?, ?, ?, ?)",
                (user_id, phone, name, "user", 1)
            )
            user = {
                "id": user_id,
                "phone_number": phone,
                "full_name": name,
                "avatar_url": None,
                "role": "user",
                "is_verified": True
            }
        
        profile = UserProfile(
            id=user["id"],
            phone_number=user["phone_number"],
            full_name=user["full_name"],
            avatar_url=user["avatar_url"],
            role=user["role"],
            is_verified=bool(user["is_verified"])
        )
        
        return AuthTokenResponse(
            access_token=f"jwt-mock-token-for-{user['id']}",
            user=profile
        )

@router.get("/users", response_model=List[UserProfile], summary="Mavjud foydalanuvchilar (Demo)")
def list_demo_users():
    with get_db() as db:
        db.execute("SELECT id, phone_number, full_name, avatar_url, role, is_verified FROM users ORDER BY created_at DESC")
        rows = db.fetchall()
        return [UserProfile(**{**r, "is_verified": bool(r["is_verified"])}) for r in rows]
