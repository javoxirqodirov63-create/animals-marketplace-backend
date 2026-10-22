"""
Universal Hayvonlar Bozori (Animals-uz) - Telegram Bot
Ushbu bot ma'lumotlar bazasi bilan to'liq integratsiyalashgan.
Xavfsizlik: Admin Panel va ichki havolalar oddiy foydalanuvchilardan 100% yashirilgan!
"""

import asyncio
import os
import sys
import json
import sqlite3
from pathlib import Path

# Windows konsolida UTF-8 ni ta'minlash
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import httpx

# Bot Token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8876952734:AAHhItlxD_jfYvEPUUnqLdUYaZuHHUozmGw")

# Xavfsizlik: Faqat sizning shaxsiy Telegram ID raqamingiz Admin hisoblanadi
ADMIN_IDS = [8957417494]

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
            payload["reply_markup"] = reply_markup

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(f"{self.api_url}/sendMessage", json=payload, timeout=10.0)
                print(f"[*] sendMessage javobi: {res.status_code} -> {res.text[:120]}", flush=True)
                return res.json()
            except Exception as e:
                print(f"[!] Xabar yuborishda xato: {e}", flush=True)
                return None

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
        is_admin = chat_id in ADMIN_IDS

        print(f"[*] Yangi xabar keldi: chat_id={chat_id} (Admin: {is_admin}), text='{text}'", flush=True)

        # Oddiy foydalanuvchilar uchun xavfsiz va toza menyu
        user_keyboard = {
            "keyboard": [
                [{"text": "🐾 Barcha E'lonlar"}, {"text": "🔍 Qidirish"}],
                [{"text": "ℹ️ Ilova haqida"}, {"text": "📞 Aloqa / Yordam"}]
            ],
            "resize_keyboard": True,
            "persistent": True
        }

        # Faqat Admin uchun maxsus menyu (Admin paneli va boshqaruv bilan)
        admin_keyboard = {
            "keyboard": [
                [{"text": "🐾 Barcha E'lonlar"}, {"text": "🔍 Qidirish"}],
                [{"text": "👑 Admin Boshqaruv"}, {"text": "📊 Maxfiy Statistika"}]
            ],
            "resize_keyboard": True,
            "persistent": True
        }

        active_keyboard = admin_keyboard if is_admin else user_keyboard

        if text.startswith("/start"):
            welcome_text = (
                f"Assalomu alaykum, <b>{first_name}</b>!\n\n"
                "🐾 <b>Universal Hayvonlar Bozori (Animals-uz)</b> rasmiy botiga xush kelibsiz!\n\n"
                "Bu yerda siz O'zbekiston bo'yicha barcha turdagi chorva mollari, uy hayvonlari va parrandalarni topishingiz va sotuvchilar bilan to'g'ridan-to'g'ri bog'lanishingiz mumkin.\n\n"
                "👇 Kerakli bo'limni tanlang yoki qidirayotgan hayvoningiz nomini yozing (masalan: <i>Sigir</i>, <i>Alabay</i>, <i>Ot</i>, <i>Qo'chqor</i>):"
            )
            await self.send_message(chat_id, welcome_text, active_keyboard)

        elif text in ["/all", "🐾 Barcha E'lonlar"]:
            listings = self.search_listings("")
            await self.send_message(chat_id, "📋 <b>So'nggi faol e'lonlar:</b>")
            for item in listings:
                vip_badge = "⭐ <b>[VIP E'LON]</b>\n" if item["is_vip"] else ""
                msg = (
                    f"{vip_badge}"
                    f"📌 <b>{item['title']}</b>\n"
                    f"💰 <b>Narxi:</b> {item['price']:,.0f} {item['currency']}\n"
                    f"🏷 <b>Zoti:</b> {item['breed'] or 'Oddiy'}\n"
                    f"📍 <b>Manzil:</b> {item['location']}\n"
                    f"👤 <b>Sotuvchi:</b> {item['seller_name']}\n"
                    f"📞 <b>Aloqa:</b> <code>{item['contact_phone']}</code>\n"
                )
                await self.send_message(chat_id, msg)

        elif text in ["ℹ️ Ilova haqida"]:
            about_text = (
                "ℹ️ <b>Animals-uz Platformasi Haqida:</b>\n\n"
                "Ushbu platforma O'zbekistondagi barcha turdagi hayvonlar savdosini osonlashtirish maqsadida yaratilgan.\n\n"
                "✅ <b>Asosiy afzalliklari:</b>\n"
                "• O'rtakashlarsiz, to'g'ridan-to'g'ri sotuvchi bilan bog'lanish;\n"
                "• Viloyat va tumanlar bo'yicha qulay qidiruv;\n"
                "• Chorva, uy hayvonlari va parrandalar bitta joyda."
            )
            await self.send_message(chat_id, about_text, active_keyboard)

        elif text in ["/help", "📞 Aloqa / Yordam", "📞 Aloqa"]:
            help_text = (
                "📞 <b>Mijozlarni Qo'llab-Quvvatlash:</b>\n\n"
                "Savollar, takliflar yoki e'lon joylash bo'yicha yordam kerak bo'lsa, administrator bilan bog'lanishingiz mumkin:\n"
                "👤 Telegram: @javoxirqodirov63"
            )
            await self.send_message(chat_id, help_text, active_keyboard)

        elif text in ["🔍 Qidirish"]:
            await self.send_message(
                chat_id,
                "🔍 Qidirayotgan hayvoningiz nomini yozing (masalan: <b>Alabay</b>, <b>Sigir</b>, <b>Ot</b> yoki <b>Hisori</b>):",
                active_keyboard
            )

        # FAQAT ADMIN UCHUN BUYRUQLAR (Oddiy foydalanuvchilarga ko'rinmaydi va ishlamaydi)
        elif text in ["/admin", "👑 Admin Boshqaruv"]:
            if not is_admin:
                await self.send_message(chat_id, "❌ Kechirasiz, sizda admin huquqi yo'q.", user_keyboard)
                return

            admin_text = (
                "👑 <b>Hurmatli Administrator!</b>\n\n"
                "Sizning shaxsiy boshqaruv kabinetingiz:\n"
                "👉 <b>Boshqaruv Paneli:</b> http://127.0.0.1:8000/admin\n\n"
                "<i>(Ushbu havola faqat sizga ko'rinadi va oddiy foydalanuvchilarga yuborilmaydi)</i>"
            )
            await self.send_message(chat_id, admin_text, admin_keyboard)

        elif text in ["/stats", "📊 Maxfiy Statistika"]:
            if not is_admin:
                await self.send_message(chat_id, "❌ Kechirasiz, sizda admin huquqi yo'q.", user_keyboard)
                return

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
                "📊 <b>Administrator Statistikasi:</b>\n\n"
                f"• 🟢 Faol e'lonlar: <b>{active} ta</b>\n"
                f"• ⭐ VIP e'lonlar: <b>{vip} ta</b>\n"
                f"• 👥 Jami foydalanuvchilar: <b>{users} ta</b>"
            )
            await self.send_message(chat_id, stats_text, admin_keyboard)

        else:
            # Matn bo'yicha qidiruv
            listings = self.search_listings(text)
            if not listings:
                await self.send_message(
                    chat_id,
                    f"❌ <i>'{text}'</i> bo'yicha hech qanday e'lon topilmadi.\nBoshqa so'z bilan qidirib ko'ring (masalan: Sigir, Ot, Alabay).",
                    active_keyboard
                )
            else:
                await self.send_message(chat_id, f"🔍 <b>'{text}'</b> bo'yicha topilgan natijalar:")
                for item in listings:
                    vip_badge = "⭐ <b>[VIP E'LON]</b>\n" if item["is_vip"] else ""
                    msg = (
                        f"{vip_badge}"
                        f"📌 <b>{item['title']}</b>\n"
                        f"💰 <b>Narxi:</b> {item['price']:,.0f} {item['currency']}\n"
                        f"📍 <b>Manzil:</b> {item['location']}\n"
                        f"👤 <b>Sotuvchi:</b> {item['seller_name']}\n"
                        f"📞 <b>Aloqa:</b> <code>{item['contact_phone']}</code>\n"
                    )
                    await self.send_message(chat_id, msg)

    async def run(self):
        print("=" * 60, flush=True)
        print(" [*] TELEGRAM BOT ISHGA TUSHMOQDA (XAVFSIZ REJIM)...", flush=True)
        print("=" * 60, flush=True)
        
        async with httpx.AsyncClient() as client:
            try:
                me = await client.get(f"{self.api_url}/getMe", timeout=10.0)
                if me.status_code != 200:
                    print(f"[!] Xatolik: Bot tokeni xato! {me.text}", flush=True)
                    return
                bot_info = me.json()["result"]
                print(f"[*] Bot muvaffaqiyatli ulandi: @{bot_info['username']} ({bot_info['first_name']})", flush=True)
                print(f"[*] Asosiy Administrator ID: {ADMIN_IDS}", flush=True)
                print("[*] Yangi xabarlar kutilmoqda...", flush=True)
            except Exception as e:
                print(f"[!] Ulanishda xato: {e}", flush=True)
                return

        while True:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(
                        f"{self.api_url}/getUpdates",
                        params={"offset": self.offset, "timeout": 15},
                        timeout=20.0
                    )
                    if res.status_code == 200:
                        updates = res.json().get("result", [])
                        for update in updates:
                            self.offset = update["update_id"] + 1
                            if "message" in update:
                                await self.handle_message(update["message"])
            except Exception as e:
                print(f"[!] Polling xatosi: {e}", flush=True)
                await asyncio.sleep(2)
            await asyncio.sleep(0.3)

if __name__ == "__main__":
    bot = TelegramBot(BOT_TOKEN)
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\nBot to'xtatildi.", flush=True)
