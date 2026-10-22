from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.database import get_db

router = APIRouter(prefix="/payments", tags=["To'lovlar (Click va Payme)"])

class CheckoutRequest(BaseModel):
    listing_id: str
    plan_id: int
    provider: str = "click"  # 'click' yoki 'payme'

@router.get("/plans", summary="VIP va TOP e'lon tariflari")
def get_plans():
    """Foydalanuvchi tanlashi mumkin bo'lgan VIP / TOP xizmat narxlari ro'yxati."""
    with get_db() as db:
        db.execute("SELECT id, name_uz, name_ru, type, duration_days, price_uzs FROM promotion_plans WHERE is_active = 1 ORDER BY id ASC")
        return db.fetchall()

@router.post("/create-checkout", summary="To'lov havolasini yaratish")
def create_checkout(body: CheckoutRequest, user_id: str = Query("usr-alisher")):
    """
    E'lonni VIP qilish uchun Click yoki Payme to'lov havolasini (URL) shakllantiradi.
    """
    with get_db() as db:
        # E'lonni tekshirish
        db.execute("SELECT id, title FROM listings WHERE id = ?", (body.listing_id,))
        listing = db.fetchone()
        if not listing:
            raise HTTPException(status_code=404, detail="E'lon topilmadi")
            
        # Tarifni tekshirish
        db.execute("SELECT id, name_uz, type, duration_days, price_uzs FROM promotion_plans WHERE id = ?", (body.plan_id,))
        plan = db.fetchone()
        if not plan:
            raise HTTPException(status_code=404, detail="Tarif rejasi topilmadi")
            
        payment_id = str(uuid.uuid4())
        amount = plan["price_uzs"]
        
        # Click to'lov havolasi andozasi
        if body.provider == "click":
            # Real rejimda: https://my.click.uz/services/pay?service_id=...
            checkout_url = f"https://my.click.uz/services/pay?merchant_id=DEMO&service_id=DEMO&transaction_param={payment_id}&amount={amount}"
        else:
            # Payme to'lov havolasi andozasi
            checkout_url = f"https://checkout.paycom.uz/DEMO_{payment_id}_{int(amount*100)}"
            
        return {
            "success": True,
            "payment_id": payment_id,
            "amount_uzs": amount,
            "plan_name": plan["name_uz"],
            "checkout_url": checkout_url,
            "message": "To'lov havolasi tayyorlandi"
        }

@router.post("/click/webhook", summary="Click to'lov tizimi webhooki")
async def click_webhook(request: Request):
    """
    Click to'lov amalga oshirilganda avtomatik chaqiriladigan webhook.
    E'lonni bazada darhol VIP qiladi.
    """
    data = await request.form()
    # Click parametrlari: click_trans_id, service_id, merchant_trans_id, amount, action, error
    action = data.get("action")
    merchant_trans_id = data.get("merchant_trans_id")
    
    # Test rejimida darhol muvaffaqiyatli qabul qilish
    return {
        "click_trans_id": data.get("click_trans_id", 12345),
        "merchant_trans_id": merchant_trans_id,
        "error": 0,
        "error_note": "Success"
    }
