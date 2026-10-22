"""
Universal Hayvonlar Bozori (Animals-uz) - Telegram Bot
Ushbu bot FastAPI va ma'lumotlar bazasi bilan to'g'ridan-to'g'ri integratsiyalashgan.
Hech qanday qo'shimcha og'ir kutubxona shart emas (mavjud httpx orqali ishlaydi).
"""

import asyncio
import os
import sys
import json
import sqlite3
from pathlib import Path

# Windows konsoli uchun UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import httpx

# Bot Token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8876952734:AAHhItlxD_jfYvEPUUnqLdUYaZuHHUozmGw")

# WebApp URL (agar internet domeni bo'lsa o'shani, bo'lmasa ko'rsatma)
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:7777")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")

# Baza yo'li
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "marketplace_demo.db"

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0

    async def send_message(self, chat_id: int, text: str, reply_markup=None):
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
            
        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"{self.api_url}/sendMessage", json=payload, timeout=10.0)
            except Exception as e:
                print(f"[!] Xabar yuborishda xato: {e}")

    async def send_photo(self, chat_id: int, photo_url: str, caption: str, reply_markup=None):
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(f"{self.api_url}/sendPhoto", json=payload, timeout=10.0)
                if res.status_code != 200:
                    # Agar rasm ochilmasa oddiy matn qilib yuboramiz
                    await self.send_message(chat_id, caption, reply_markup)
            except Exception:
                await self.send_message(chat_id, caption, reply_markup)

    def search_listings(self, query: str = ""):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        sql = """
        SELECT 
            l.id, l.title, l.price, l.currency, l.breed, l.contact_phone, l.is_vip,
            c.name_uz AS category_name,
            r.name_uz || ', ' || d.name_uz AS location,
            u.full_name AS seller_name
        FROM listings l
        JOIN categories c ON l.category_id = c.id
        JOIN districts d ON l.district_id = d.id
        JOIN regions r ON d.region_id = r.id
        JOIN users u ON l.seller_id = u.id
        WHERE l.status = 'active'
        """
        params = []
        if query:
            sql += " AND (l.title LIKE ? OR l.description LIKE ? OR l.breed LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
            
        sql += " ORDER BY l.is_vip DESC, l.created_at DESC LIMIT 5"
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()
        return results

    async def handle_message(self, message: dict):
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        first_name = message["chat"].get("first_name", "Foydalanuvchi")

        if text.startswith("/start"):
            welcome_text = (
                f"Assalomu alaykum, <b>{first_name}</b>!\n\n"
                "🐾 <b>Universal Hayvonlar Bozori (Animals-uz)</b> rasmiy botiga xush kelibsiz!\n\n"
                "Ushbu bot orqali siz O'zbekiston bo'yicha barcha turdagi chorva mollari, uy hayvonlari va parrandalarni sotishingiz yoki sotib olishingiz mumkin.\n\n"
                "👇 Kerakli bo'limni tanlang yoki qidirayotgan hayvoningiz nomini yozing (masalan: <i>Alabay</i> yoki <i>Sigir</i>):"
            )
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🚀 Bozorga Kirish (Ilovani Ochish)", "web_app": {"url": WEBAPP_URL}}],
                    [{"text": "📋 Barcha E'lonlar", "callback_data": "all_listings"}],
                    [{"text": "👑 Boshqaruv (Admin)", "url": "http://127.0.0.1:8000/admin"}]
                ]
            }
            await self.send_message(chat_id, welcome_text, keyboard)

        elif text == "/stats":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM listings WHERE status = 'active'")
            active = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM listings WHERE is_vip = 1")
            vip = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM users")
            users = c.fetchone()[0]
            conn.close()
            
            stats_text = (
                "📊 <b>Platforma Statistikasi:</b>\n\n"
                f"• Faol e'lonlar: <b>{active} ta</b>\n"
                f"• VIP e'lonlar: <b>{vip} ta</b>\n"
                f"• Foydalanuvchilar: <b>{users} ta</b>"
            )
            await self.send_message(chat_id, stats_text)

        else:
            # Matn bo'yicha qidiruv
            listings = self.search_listings(text)
            if not listings:
                await self.send_message(
                    chat_id,
                    f"❌ Kechirasiz, <i>'{text}'</i> bo'yicha hech qanday e'lon topilmadi.\nBoshqa so'z bilan qidirib ko'ring (masalan: Sigir, Ot, Alabay, Qo'chqor)."
                )
            else:
                await self.send_message(chat_id, f"🔍 <b>'{text}'</b> bo'yicha topilgan e'lonlar:")
                for item in listings:
                    vip_badge = "⭐ <b>VIP E'LON</b>\n" if item["is_vip"] else ""
                    msg = (
                        f"{vip_badge}"
                        f"📌 <b>{item['title']}</b>\n"
                        f"💰 <b>Narxi:</b> {item['price']:,.0f} {item['currency']}\n"
                        f"📍 <b>Manzil:</b> {item['location']}\n"
                        f"👤 <b>Sotuvchi:</b> {item['seller_name']}\n"
                        f"📞 <b>Telefon:</b> {item['contact_phone']}\n"
                    )
                    await self.send_message(chat_id, msg)

    async def run(self):
        print("=" * 60, flush=True)
        print(" [*] TELEGRAM BOT ISHGA TUSHMOQDA...", flush=True)
        print("=" * 60, flush=True)
        
        async with httpx.AsyncClient() as client:
            try:
                me = await client.get(f"{self.api_url}/getMe", timeout=10.0)
                if me.status_code != 200:
                    print("[!] Xatolik: Bot tokeni noto'g'ri yoki yaroqsiz!", flush=True)
                    return
                bot_info = me.json()["result"]
                print(f"[*] Bot muvaffaqiyatli ulandi: @{bot_info['username']} ({bot_info['first_name']})", flush=True)
                print("[*] Yangi xabarlar kutilmoqda...", flush=True)
            except Exception as e:
                print(f"[!] Ulanishda xato: {e}", flush=True)
                return

        while True:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(
                        f"{self.api_url}/getUpdates",
                        params={"offset": self.offset, "timeout": 20},
                        timeout=25.0
                    )
                    if res.status_code == 200:
                        updates = res.json().get("result", [])
                        for update in updates:
                            self.offset = update["update_id"] + 1
                            if "message" in update:
                                await self.handle_message(update["message"])
                            elif "callback_query" in update:
                                cb = update["callback_query"]
                                if cb.get("data") == "all_listings":
                                    listings = self.search_listings("")
                                    for item in listings:
                                        msg = (
                                            f"📌 <b>{item['title']}</b>\n"
                                            f"💰 Narxi: {item['price']:,.0f} {item['currency']}\n"
                                            f"📍 Manzil: {item['location']}\n"
                                            f"📞 Tel: {item['contact_phone']}"
                                        )
                                        await self.send_message(cb["message"]["chat"]["id"], msg)
            except Exception as e:
                await asyncio.sleep(2)
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    token = BOT_TOKEN
    if not token and len(sys.argv) > 1:
        token = sys.argv[1]
        
    if not token:
        print("[!] Iltimos, Telegram Bot Tokenini kiriting!")
        print("Foydalanish: python bot.py <SIZNING_BOT_TOKENINGIZ>")
        sys.exit(1)
        
    bot = TelegramBot(token)
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\nBot to'xtatildi.")
