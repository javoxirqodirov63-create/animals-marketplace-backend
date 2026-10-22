"""
FastAPI Backend API Avtomatik Sinov Skripti
Barcha asosiy endpointlarni birma-bir tekshiradi:
1. Root / healthcheck
2. Viloyatlar va Tumanlar (/api/locations)
3. Kategoriyalar daraxti (/api/categories)
4. SMS OTP avtorizatsiya (/api/auth)
5. E'lonlar lentasi va qidiruv (/api/listings)
6. Sevimlilarga qo'shish (/api/listings/{id}/favorite)
7. Ichki chat (/api/chat)
"""

import sys
import os

# Papka yo'lini qo'shish
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Windows konsoli uchun UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 65)
    print(" 🧪 FASTAPI BACKEND ENDPOINTLARINI SINOVDAN O'TKAZISH")
    print("=" * 65)
    
    # 1. Healthcheck
    res = client.get("/")
    assert res.status_code == 200
    print("✅ [1/7] Healthcheck (GET /) -> 200 OK")
    
    # 2. Viloyatlar
    res = client.get("/api/locations/regions")
    assert res.status_code == 200
    regions = res.json()
    assert len(regions) >= 14
    print(f"✅ [2/7] Viloyatlar (GET /api/locations/regions) -> {len(regions)} ta hudud yuklandi")
    
    # 3. Kategoriyalar
    res = client.get("/api/categories")
    assert res.status_code == 200
    categories = res.json()
    assert len(categories) >= 3
    print(f"✅ [3/7] Kategoriyalar daraxti (GET /api/categories) -> {len(categories)} ta asosiy toifa")
    
    # 4. Auth: SMS OTP
    res = client.post("/api/auth/send-otp", json={"phone_number": "+998901234567"})
    assert res.status_code == 200
    res_verify = client.post("/api/auth/verify-otp", json={"phone_number": "+998901234567", "code": "7777"})
    assert res_verify.status_code == 200
    token = res_verify.json()["access_token"]
    print(f"✅ [4/7] SMS OTP Login (/api/auth/verify-otp) -> Token: {token[:15]}...")
    
    # 5. E'lonlar lentasi (VIP birinchi chiqishi kerak)
    res = client.get("/api/listings")
    assert res.status_code == 200
    listings = res.json()
    assert len(listings) >= 3
    first_ad = listings[0]
    print(f"✅ [5/7] E'lonlar lentasi (GET /api/listings) -> {len(listings)} ta e'lon, 1-o'rinda: '{first_ad['title']}' (VIP: {first_ad['is_vip']})")
    
    # 6. Sevimlilarga qo'shish (Toggle favorite)
    ad_id = first_ad["id"]
    res_fav = client.post(f"/api/listings/{ad_id}/favorite?user_id=usr-dilshod")
    assert res_fav.status_code == 200
    print(f"✅ [6/7] Sevimlilar (POST /api/listings/{ad_id}/favorite) -> {res_fav.json()['message']}")
    
    # 7. Chat xabarlari
    res_conv = client.get("/api/chat/conversations?user_id=usr-dilshod")
    assert res_conv.status_code == 200
    convs = res_conv.json()
    assert len(convs) >= 1
    conv_id = convs[0]["id"]
    res_msg = client.get(f"/api/chat/conversations/{conv_id}/messages")
    assert res_msg.status_code == 200
    messages = res_msg.json()
    print(f"✅ [7/7] Ichki Chat (/api/chat) -> Suhbat topildi ({len(messages)} ta xabar)")

    print("\n" + "=" * 65)
    print(" 🎉 BARCHA FASTAPI ENDPOINTLARI 100% MUVAFFAQIYATLI ISHLADI!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
