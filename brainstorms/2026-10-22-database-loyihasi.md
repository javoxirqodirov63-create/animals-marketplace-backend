# Hayvonlar Oldi-Sotdi Ilovasi (Pet & Livestock Marketplace): Brainstorm va Rejalashtirish Qaydlari
Sana: 2026-10-22 · Maqsad: Universal hayvonlar oldi-sotdisi (uy hayvonlari, chorva, parranda) platformasi uchun ma'lumotlar bazasi, Backend API, Mobil Ilova va Admin Panelni birlashtirish.
Holat: TO'LIQ ISHGA TUSHDI (Database + FastAPI Backend + Flutter Mobile App + Web Admin Panel jonli ishlamoqda)

## Asosiy tizimlar va manzillar:
- **Admin Boshqaruv Paneli:** `http://127.0.0.1:8000/admin` (Statistika, VIP/Bloklash boshqaruvi, foydalanuvchilar, shikoyatlar).
- **Mobil Ilova (Flutter Web):** `http://localhost:7777` (Mijozlar e'lon ko'rish va berish platformasi).
- **Backend Swagger API:** `http://127.0.0.1:8000/docs` (Interaktiv REST API hujjatlari).
- **Lokal Ma'lumotlar Bazasi:** `marketplace_demo.db` (Barcha 13 ta asosiy jadval bilan).

## Yaratilgan Fayllar:
1. `backend/app/routers/admin.py` — Admin panel API endpointlari va statistikalar.
2. `backend/app/templates/admin.html` — Zamonaviy Tailwind CSS asosidagi to'liq boshqaruv sahifasi.
3. `start_all.bat` — Barcha tizimlarni (Backend + Flutter) bir bosishda ishga tushiruvchi yorliq.
4. `schema.sql` va `seed.sql` — PostgreSQL DDL va O'zbekiston ma'lumotlari.
5. `README.md` — To'liq tizim hujjatlari.
