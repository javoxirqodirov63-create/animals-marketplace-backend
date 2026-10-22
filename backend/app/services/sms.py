import httpx
import os
from typing import Optional

ESKIZ_EMAIL = os.getenv("ESKIZ_EMAIL", "")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD", "")

class SMSService:
    """
    Eskiz.uz SMS shlyuzi integratsiyasi.
    Hozirgi ishlab chiqish (dev) rejimida kodlarni konsolga chiqaradi.
    Real Eskiz tokeni kiritilganda haqiqiy SMS yuboradi.
    """
    TOKEN_URL = "https://notify.eskiz.uz/api/auth/login"
    SEND_URL = "https://notify.eskiz.uz/api/message/sms/send"
    _token: Optional[str] = None

    @classmethod
    async def get_token(cls) -> Optional[str]:
        if not ESKIZ_EMAIL or not ESKIZ_PASSWORD:
            return None
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(cls.TOKEN_URL, data={
                    "email": ESKIZ_EMAIL,
                    "password": ESKIZ_PASSWORD
                }, timeout=5.0)
                if res.status_code == 200:
                    cls._token = res.json().get("data", {}).get("token")
                    return cls._token
        except Exception:
            return None
        return None

    @classmethod
    async def send_otp_sms(cls, phone_number: str, code: str) -> bool:
        # Agar Eskiz kalitlari ulanmagan bo'lsa, xavfsiz dev rejimida ishlaydi
        if not ESKIZ_EMAIL:
            print(f"[*] DEV REJIMI: [SMS OTP] -> {phone_number} uchun tasdiqlash kodi: {code}")
            return True
            
        token = cls._token or await cls.get_token()
        if not token:
            print(f"[!] Eskiz tokeni olinmadi, dev kod: {code}")
            return False

        message = f"Universal Hayvonlar Bozori. Tasdiqlash kodingiz: {code}"
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    cls.SEND_URL,
                    headers={"Authorization": f"Bearer {token}"},
                    data={
                        "mobile_phone": phone_number.replace("+", ""),
                        "message": message,
                        "from": "4546"
                    },
                    timeout=5.0
                )
                return res.status_code == 200
        except Exception as e:
            print(f"[!] SMS yuborishda xato: {e}")
            return False
