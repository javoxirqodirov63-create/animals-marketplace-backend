"""
Universal Hayvonlar Bozori - SQLite Demo & To'liq Sinov Skripti
Ushbu skript PostgreSQL arxitekturasini SQLite faylida sinab ko'rish imkonini beradi.
Hech qanday qo'shimcha kutubxona o'rnatish shart emas.
"""

import sqlite3
import json
import os
import sys

# Windows konsolida UTF-8 matn chiqishini ta'minlash
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_FILE = "marketplace_demo.db"

if os.path.exists(DB_FILE):
    try:
        os.remove(DB_FILE)
    except Exception:
        pass

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 1. Jadvallarni yaratish
cursor.executescript("""
CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_uz TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE districts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL REFERENCES regions(id),
    name_uz TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    slug TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    UNIQUE(region_id, slug)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER REFERENCES categories(id),
    name_uz TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    phone_number TEXT NOT NULL UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'user',
    is_verified INTEGER DEFAULT 0
);

CREATE TABLE listings (
    id TEXT PRIMARY KEY,
    seller_id TEXT NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    district_id INTEGER NOT NULL REFERENCES districts(id),
    title TEXT NOT NULL,
    slug TEXT,
    description TEXT NOT NULL,
    price REAL DEFAULT 0.0,
    currency TEXT DEFAULT 'UZS',
    price_type TEXT DEFAULT 'fixed',
    breed TEXT,
    gender TEXT,
    age_months INTEGER,
    is_vaccinated INTEGER DEFAULT 0,
    has_pedigree INTEGER DEFAULT 0,
    attributes TEXT,
    contact_phone TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    is_vip INTEGER DEFAULT 0,
    is_top INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    favorites_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE listing_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id TEXT NOT NULL REFERENCES listings(id),
    image_url TEXT NOT NULL,
    is_primary INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL REFERENCES users(id),
    listing_id TEXT NOT NULL REFERENCES listings(id),
    UNIQUE(user_id, listing_id)
);

CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    listing_id TEXT REFERENCES listings(id),
    buyer_id TEXT NOT NULL REFERENCES users(id),
    seller_id TEXT NOT NULL REFERENCES users(id),
    last_message_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL REFERENCES conversations(id),
    sender_id TEXT NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE listing_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id TEXT NOT NULL REFERENCES listings(id),
    reporter_id TEXT NOT NULL REFERENCES users(id),
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE promotion_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_uz TEXT NOT NULL,
    type TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    price_uzs REAL NOT NULL
);

-- Trigger: Sevimlilar sonini yangilash
CREATE TRIGGER trg_fav_insert AFTER INSERT ON favorites
BEGIN
    UPDATE listings SET favorites_count = favorites_count + 1 WHERE id = NEW.listing_id;
END;

CREATE TRIGGER trg_fav_delete AFTER DELETE ON favorites
BEGIN
    UPDATE listings SET favorites_count = MAX(0, favorites_count - 1) WHERE id = OLD.listing_id;
END;
""")

# 2. O'zbekiston viloyatlari
regions_data = [
    (1, 'Toshkent shahri', 'г. Ташкент', 'toshkent-shahar', 1),
    (2, 'Toshkent viloyati', 'Ташкентская область', 'toshkent-viloyati', 2),
    (3, 'Andijon viloyati', 'Андижанская область', 'andijon', 3),
    (4, 'Buxoro viloyati', 'Бухарская область', 'buxoro', 4),
    (5, 'Farg''ona viloyati', 'Ферганская область', 'fargona', 5),
    (6, 'Jizzax viloyati', 'Джизакская область', 'jizzax', 6),
    (7, 'Xorazm viloyati', 'Хорезмская область', 'xorazm', 7),
    (8, 'Namangan viloyati', 'Наманганская область', 'namangan', 8),
    (9, 'Navoiy viloyati', 'Навоийская область', 'navoiy', 9),
    (10, 'Qashqadaryo viloyati', 'Кашкадарьинская область', 'qashqadaryo', 10),
    (11, 'Samarqand viloyati', 'Самаркандская область', 'samarqand', 11),
    (12, 'Sirdaryo viloyati', 'Сырдарьинская область', 'sirdaryo', 12),
    (13, 'Surxondaryo viloyati', 'Сурхандарьинская область', 'surxondaryo', 13),
    (14, 'Qoraqalpog''iston Respublikasi', 'Республика Каракалпакстан', 'qoraqalpogiston', 14)
]
cursor.executemany("INSERT INTO regions VALUES (?, ?, ?, ?, ?)", regions_data)

# 3. Tumanlar
districts_data = [
    (1, 1, 'Yunusobod tumani', 'Юнусабадский район', 'yunusobod', 1),
    (2, 1, 'Chilonzor tumani', 'Чиланзарский район', 'chilonzor', 2),
    (3, 1, 'Mirzo Ulug''bek tumani', 'Мирзо-Улугбекский район', 'mirzo-ulugbek', 3),
    (4, 2, 'Bo''stonliq tumani', 'Бостанлыкский район', 'bostonliq', 1),
    (5, 2, 'Zangiota tumani', 'Зангиатинский район', 'zangiota', 2),
    (6, 11, 'Samarqand shahri', 'г. Самарканд', 'samarqand-shahar', 1),
    (7, 11, 'Urgut tumani', 'Ургутский район', 'urgut', 2),
    (8, 3, 'Andijon shahri', 'г. Андижан', 'andijon-shahar', 1),
    (9, 5, 'Farg''ona shahri', 'г. Фергана', 'fargona-shahar', 1)
]
cursor.executemany("INSERT INTO districts VALUES (?, ?, ?, ?, ?, ?)", districts_data)

# 4. Kategoriyalar
categories_data = [
    (1, None, 'Chorva mollari', 'Сельхоз животные', 'chorva', 1),
    (2, None, 'Uy hayvonlari', 'Домашние питомцы', 'uy-hayvonlari', 2),
    (3, None, 'Parrandalar', 'Птицы', 'parrandalar', 3),
    (4, 1, 'Qoramol (Sigir, Buqa)', 'КРС', 'qoramol', 1),
    (5, 1, 'Qo''y va Echkilar (Hisori)', 'Овцы и козы', 'qoy-echki', 2),
    (6, 1, 'Otlar va Yilqilar', 'Лошади', 'otlar', 3),
    (7, 2, 'Itlar va Kuchukchalar', 'Собаки', 'itlar', 1),
    (8, 2, 'Mushuklar va Mushukchalar', 'Кошки', 'mushuklar', 2)
]
cursor.executemany("INSERT INTO categories (id, parent_id, name_uz, name_ru, slug, sort_order) VALUES (?, ?, ?, ?, ?, ?)", categories_data)

# 5. Foydalanuvchilar
users_data = [
    ('usr-admin', '+998901234567', 'Tizim Administratori', None, 'admin', 1),
    ('usr-alisher', '+998935557799', 'Alisher Chorvador', None, 'user', 1),
    ('usr-dilshod', '+998971112233', 'Dilshod PetLover', None, 'user', 1),
    ('usr-jasur', '+998998884422', 'Jasur Otboqar', None, 'user', 1)
]
cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", users_data)

# 6. E'lonlar
listings_data = [
    (
        'lst-1', 'usr-alisher', 4, 6,
        'Goloshtin zotli 1-qorin sog''in sigir, 26L sut',
        'goloshtin-sogin-sigir-26l',
        'Toza qonli Goloshtin sigir sotiladi. Emlangan, kuniga 26 litr sut beradi.',
        28000000.0, 'UZS', 'negotiable', 'Goloshtin', 'female', 30, 1, 1,
        json.dumps({"daily_milk_liters": 26, "calving_count": 1}),
        '+998935557799', 'active', 1, 1, 145, 12
    ),
    (
        'lst-2', 'usr-dilshod', 7, 2,
        'Toza qonli Oq Alabay kuchukchalari, pasporti bor',
        'oq-alabay-kuchukchalari-pasport',
        '2 oylik baquvvat Alabay bolalari. Nobivac qilingan, pasportli.',
        3500000.0, 'UZS', 'fixed', 'Alabay', 'male', 2, 1, 1,
        json.dumps({"color": "Oq-sariq", "puppy_count": 5}),
        '+998971112233', 'active', 1, 0, 94, 8
    ),
    (
        'lst-3', 'usr-alisher', 5, 7,
        'Nasldor Hisori semiz qo''chqor, 95 kg tirik vaznda',
        'hisori-semiz-qochqor-95kg',
        'Urgutda boqilgan nasldor Hisori qo''chqor. Makkajo''xori va bedada boqilgan.',
        5800000.0, 'UZS', 'negotiable', 'Hisori', 'male', 18, 1, 0,
        json.dumps({"live_weight_kg": 95}),
        '+998935557799', 'active', 0, 1, 72, 5
    ),
    (
        'lst-4', 'usr-jasur', 6, 4,
        'Ko''pkari (Uloq) uchun tayyor Qorabayir to''riq ayg''ir',
        'kopkari-qorabayir-toriq-aygir',
        '5 yoshli chopqir, baquvvat uloqchi ot. Barcha hujjatlari bor.',
        45000000.0, 'UZS', 'negotiable', 'Qorabayir', 'male', 60, 1, 1,
        json.dumps({"suit": "To''riq", "withers_height_cm": 162}),
        '+998998884422', 'active', 1, 1, 210, 19
    ),
    (
        'lst-5', 'usr-dilshod', 8, 1,
        'Shotland vislouxim (Scottish Fold) moviy mushukcha',
        'shotland-vislouxim-mushukcha',
        '1.5 oylik go''zal zotli mushukcha. Qumga o''rgatilgan, erka va o''yinqaroq.',
        1200000.0, 'UZS', 'fixed', 'Scottish Fold', 'female', 1, 0, 0,
        json.dumps({"fur_color": "Moviy kulrang"}),
        '+998971112233', 'active', 0, 0, 48, 3
    )
]

cursor.executemany("""
INSERT INTO listings (
    id, seller_id, category_id, district_id, title, slug, description,
    price, currency, price_type, breed, gender, age_months, is_vaccinated,
    has_pedigree, attributes, contact_phone, status, is_vip, is_top,
    views_count, favorites_count
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", listings_data)

# 7. Demo Chat va Xabarlar
cursor.execute("""
INSERT INTO conversations (id, listing_id, buyer_id, seller_id, last_message_text)
VALUES ('conv-1', 'lst-2', 'usr-alisher', 'usr-dilshod', 'Kuchukchalardan qoldimi?')
""")

cursor.executescript("""
INSERT INTO messages (conversation_id, sender_id, content, is_read)
VALUES 
('conv-1', 'usr-alisher', 'Assalomu alaykum! Kuchukchalardan qoldimi?', 1),
('conv-1', 'usr-dilshod', 'Vaalaykum assalom! Ha, 3 ta oq kuchukcha bor.', 0);
""")

conn.commit()

print("=" * 70)
print(" UNIVERSAL HAYVONLAR BOZORI - BAZA TESTI MUVAFFAQIYATLI O'TDI!")
print("=" * 70)

# TEST 1: Asosiy lenta (VIP e'lonlar oldinda)
print("\n[TEST 1] Asosiy sahifa lentasi (VIP va TOP e'lonlar birinchi o'rinda):")
query1 = """
SELECT 
    l.title, 
    l.price, 
    l.currency, 
    c.name_uz AS kategoriya,
    r.name_uz || ', ' || d.name_uz AS manzil,
    CASE WHEN l.is_vip = 1 THEN '[VIP] ' ELSE '' END ||
    CASE WHEN l.is_top = 1 THEN '[TOP] ' ELSE '' END AS badges,
    u.full_name AS sotuvchi,
    l.contact_phone,
    l.favorites_count
FROM listings l
JOIN categories c ON l.category_id = c.id
JOIN districts d ON l.district_id = d.id
JOIN regions r ON d.region_id = r.id
JOIN users u ON l.seller_id = u.id
WHERE l.status = 'active'
ORDER BY l.is_vip DESC, l.is_top DESC, l.created_at DESC;
"""
for row in cursor.execute(query1):
    title, price, curr, cat, loc, badges, seller, phone, favs = row
    print(f"-> {badges}[{cat}] {title}")
    print(f"   Narxi: {price:,.0f} {curr} | Manzil: {loc}")
    print(f"   Sotuvchi: {seller} ({phone}) | Sevimlilar: {favs} ta\n")

# TEST 2: Samarqand viloyati bo'yicha filtr
print("-" * 70)
print("[TEST 2] Samarqand viloyatidagi barcha chorva e'lonlari:")
query2 = """
SELECT l.title, l.price, l.currency, l.breed, d.name_uz, l.attributes
FROM listings l
JOIN districts d ON l.district_id = d.id
WHERE d.region_id = 11 AND l.status = 'active';
"""
for row in cursor.execute(query2):
    title, price, curr, breed, district, attrs = row
    print(f"-> {title}")
    print(f"   Zoti: {breed} | Narxi: {price:,.0f} {curr} | Tuman: {district}")
    print(f"   Xususiyatlari: {attrs}\n")

# TEST 3: Chat xabarlari tarixi
print("-" * 70)
print("[TEST 3] Alisher va Dilshod o'rtasidagi ichki chat (Kuchukcha e'loni bo'yicha):")
query3 = """
SELECT u.full_name, m.content, m.created_at, m.is_read
FROM messages m
JOIN users u ON m.sender_id = u.id
WHERE m.conversation_id = 'conv-1'
ORDER BY m.created_at ASC;
"""
for sender, content, dt, is_read in cursor.execute(query3):
    status = "O'qildi" if is_read else "Yangi"
    print(f"[{sender}]: {content} ({status})")

conn.close()
print("\n" + "=" * 70)
