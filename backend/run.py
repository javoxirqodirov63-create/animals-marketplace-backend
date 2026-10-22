import uvicorn
import sys
import os

# Windows konsolida UTF-8 ni ta'minlash
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Papka yo'lini Python pathga qo'shish
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 65)
    print(" [*] UNIVERSAL HAYVONLAR BOZORI - FASTAPI SERVER ISHGA TUSHMOQDA")
    print(" [*] Asosiy manzil:    http://127.0.0.1:8000")
    print(" [*] API Hujjatlari:   http://127.0.0.1:8000/docs")
    print("=" * 65)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
