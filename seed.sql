-- ==============================================================================
-- Universal Hayvonlar Bozori (Pet & Livestock Marketplace)
-- Dastlabki Ma'lumotlar (Seed Data)
-- Versiya: 1.1.0
-- ==============================================================================

-- ==============================================================================
-- 1. O'ZBEKISTON VILOYATLARI (14 TA HUDUD)
-- ==============================================================================

INSERT INTO regions (id, name_uz, name_ru, slug, sort_order) VALUES
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
ON CONFLICT (id) DO NOTHING;

SELECT setval('regions_id_seq', (SELECT MAX(id) FROM regions));

-- ==============================================================================
-- 2. ASOSIY TUMANLAR VA SHAHARLAR
-- ==============================================================================

INSERT INTO districts (region_id, name_uz, name_ru, slug, sort_order) VALUES
-- Toshkent shahri (1)
(1, 'Yunusobod tumani', 'Юнусабадский район', 'yunusobod', 1),
(1, 'Chilonzor tumani', 'Чиланзарский район', 'chilonzor', 2),
(1, 'Mirzo Ulug''bek tumani', 'Мирзо-Улугбекский район', 'mirzo-ulugbek', 3),
(1, 'Yashnobod tumani', 'Яшнабадский район', 'yashnobod', 4),
(1, 'Shayxontohur tumani', 'Шайхантахурский район', 'shayxontohur', 5),
(1, 'Olmazor tumani', 'Алмазарский район', 'olmazor', 6),
(1, 'Sergeli tumani', 'Сергелийский район', 'sergeli', 7),
(1, 'Mirobod tumani', 'Мирабадский район', 'mirobod', 8),

-- Toshkent viloyati (2)
(2, 'Zangiota tumani', 'Зангиатинский район', 'zangiota', 1),
(2, 'Qibray tumani', 'Кибрайский район', 'qibray', 2),
(2, 'Chirchiq shahri', 'г. Чирчик', 'chirchiq', 3),
(2, 'Olmaliq shahri', 'г. Алмалык', 'olmaliq', 4),
(2, 'Bo''stonliq tumani', 'Бостанлыкский район', 'bostonliq', 5),
(2, 'Yangiyo''l tumani', 'Янгиюльский район', 'yangiyol', 6),

-- Andijon viloyati (3)
(3, 'Andijon shahri', 'г. Андижан', 'andijon-shahar', 1),
(3, 'Asaka tumani', 'Асакинский район', 'asaka', 2),
(3, 'Shahrixon tumani', 'Шахриханский район', 'shahrixon', 3),

-- Buxoro viloyati (4)
(4, 'Buxoro shahri', 'г. Бухара', 'buxoro-shahar', 1),
(4, 'G''ijduvon tumani', 'Гиждуванский район', 'gijduvon', 2),
(4, 'Kogon shahri', 'г. Каган', 'kogon', 3),

-- Farg'ona viloyati (5)
(5, 'Farg''ona shahri', 'г. Фергана', 'fargona-shahar', 1),
(5, 'Qo''qon shahri', 'г. Коканд', 'qoqon', 2),
(5, 'Marg''ilon shahri', 'г. Маргилан', 'margilon', 3),

-- Jizzax viloyati (6)
(6, 'Jizzax shahri', 'г. Джизак', 'jizzax-shahar', 1),
(6, 'Zomin tumani', 'Зааминский район', 'zomin', 2),

-- Xorazm viloyati (7)
(7, 'Urganch shahri', 'г. Ургенч', 'urganch-shahar', 1),
(7, 'Xiva shahri', 'г. Хива', 'xiva-shahar', 2),

-- Namangan viloyati (8)
(8, 'Namangan shahri', 'г. Наманган', 'namangan-shahar', 1),
(8, 'Chust tumani', 'Чустский район', 'chust', 2),

-- Navoiy viloyati (9)
(9, 'Navoiy shahri', 'г. Навои', 'navoiy-shahar', 1),
(9, 'Zarafshon shahri', 'г. Зарафшан', 'zarafshon', 2),

-- Qashqadaryo viloyati (10)
(10, 'Qarshi shahri', 'г. Карши', 'qarshi', 1),
(10, 'Shahrisabz shahri', 'г. Шахрисабз', 'shahrisabz', 2),
(10, 'Kitob tumani', 'Китабский район', 'kitob', 3),

-- Samarqand viloyati (11)
(11, 'Samarqand shahri', 'г. Самарканд', 'samarqand-shahar', 1),
(11, 'Pastdarg''om tumani', 'Пастдаргомский район', 'pastdargom', 2),
(11, 'Urgut tumani', 'Ургутский район', 'urgut', 3),
(11, 'Bulung''ur tumani', 'Булунгурский район', 'bulungur', 4),
(11, 'Jomboy tumani', 'Джамбайский район', 'jomboy', 5),

-- Sirdaryo viloyati (12)
(12, 'Guliston shahri', 'г. Гулистан', 'guliston', 1),
(12, 'Boyovut tumani', 'Баяутский район', 'boyovut', 2),

-- Surxondaryo viloyati (13)
(13, 'Termiz shahri', 'г. Термез', 'termiz', 1),
(13, 'Denov tumani', 'Денауский район', 'denov', 2),

-- Qoraqalpog'iston Respublikasi (14)
(14, 'Nukus shahri', 'г. Нукус', 'nukus', 1),
(14, 'Qo''ng''irot tumani', 'Кунградский район', 'qongirot', 2)
ON CONFLICT (region_id, slug) DO NOTHING;

SELECT setval('districts_id_seq', (SELECT MAX(id) FROM districts));

-- ==============================================================================
-- 3. HAYVONLAR KATEGORIYALARI (IERARXIK)
-- ==============================================================================

-- Bosh kategoriyalar
INSERT INTO categories (id, parent_id, name_uz, name_ru, slug, sort_order) VALUES
(1, NULL, 'Chorva mollari', 'Сельхоз животные / Скот', 'chorva-mollari', 1),
(2, NULL, 'Uy hayvonlari', 'Домашние питомцы', 'uy-hayvonlari', 2),
(3, NULL, 'Parrandalar', 'Птицы и птицеводство', 'parrandalar', 3),
(4, NULL, 'Boshqa jonivorlar va Mahsulotlar', 'Другие животные и товары', 'boshqa', 4)
ON CONFLICT (id) DO NOTHING;

SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));

-- 1-darajali ostkategoriyalar: Chorva mollari (parent_id = 1)
INSERT INTO categories (parent_id, name_uz, name_ru, slug, sort_order) VALUES
(1, 'Qoramol (Sigir, Buqa, Buzoq)', 'Крупный рогатый скот', 'qoramol', 1),
(1, 'Qo''y va Echkilar (Qo''chqor, Hisori)', 'Овцы и козы', 'qoy-echki', 2),
(1, 'Otlar va Yilqilar', 'Лошади', 'otlar', 3),
(1, 'Tuyalar', 'Верблюды', 'tuyalar', 4)
ON CONFLICT (slug) DO NOTHING;

-- 1-darajali ostkategoriyalar: Uy hayvonlari (parent_id = 2)
INSERT INTO categories (parent_id, name_uz, name_ru, slug, sort_order) VALUES
(2, 'Itlar va Kuchukchalar', 'Собаки и щенки', 'itlar', 1),
(2, 'Mushuklar va Mushukchalar', 'Кошки и котята', 'mushuklar', 2),
(2, 'To''tiqushlar va Sayroqi qushlar', 'Попугаи и певчие птицы', 'totiqushlar', 3),
(2, 'Akvarium baliqlari', 'Аквариумные рыбки', 'baliqlar', 4),
(2, 'Kemiruvchilar (Xomyak, Dengiz cho''chqasi)', 'Грызуны', 'kemiruvchilar', 5)
ON CONFLICT (slug) DO NOTHING;

-- 1-darajali ostkategoriyalar: Parrandalar (parent_id = 3)
INSERT INTO categories (parent_id, name_uz, name_ru, slug, sort_order) VALUES
(3, 'Tovuqlar va Xo''rozlar (Go''sht, Tuxum, Zotdor)', 'Куры и петухи', 'tovuqlar', 1),
(3, 'O''rdaklar va G''ozlar', 'Утки и гуси', 'ordak-goz', 2),
(3, 'Bedana va Kakliklar', 'Перепела и куропатки', 'bedana', 3),
(3, 'Kabutarlar (Kaptarlar)', 'Голуби', 'kabutar', 4)
ON CONFLICT (slug) DO NOTHING;

-- 1-darajali ostkategoriyalar: Boshqa jonivorlar (parent_id = 4)
INSERT INTO categories (parent_id, name_uz, name_ru, slug, sort_order) VALUES
(4, 'Quyonlar (Go''shtdor va mitti)', 'Кролики', 'quyonlar', 1),
(4, 'Asalari oilalari va qutilar', 'Пчелосемьи и ульи', 'asalari', 2),
(4, 'Hayvonlar uchun ozuqa va em-xashak', 'Корма и сено', 'ozuqa-em', 3)
ON CONFLICT (slug) DO NOTHING;

-- ==============================================================================
-- 4. VIP VA REKLAMA TARIFLARI (PROMOTION PLANS)
-- ==============================================================================

INSERT INTO promotion_plans (id, name_uz, name_ru, type, duration_days, price_uzs) VALUES
(1, 'VIP E''lon — 7 kun', 'VIP объявление — 7 дней', 'vip', 7, 35000.00),
(2, 'VIP E''lon — 30 kun', 'VIP объявление — 30 дней', 'vip', 30, 99000.00),
(3, 'TOP E''lon — 3 kun', 'В ТОП — 3 дня', 'top', 3, 15000.00),
(4, 'TOP E''lon — 7 kun', 'В ТОП — 7 дней', 'top', 7, 29000.00),
(5, 'Shoshilinch (Urgent) — 7 kun', 'Срочно — 7 дней', 'urgent', 7, 20000.00)
ON CONFLICT (id) DO NOTHING;

SELECT setval('promotion_plans_id_seq', (SELECT MAX(id) FROM promotion_plans));

-- ==============================================================================
-- 5. DEMO FOYDALANUVCHILAR
-- ==============================================================================

INSERT INTO users (id, phone_number, full_name, role, is_verified, region_id, district_id) VALUES
('11111111-1111-1111-1111-111111111111', '+998901234567', 'Tizim Administratori', 'admin', TRUE, 1, 1),
('22222222-2222-2222-2222-222222222222', '+998935557799', 'Alisher Chorvador', 'user', TRUE, 11, (SELECT id FROM districts WHERE slug = 'samarqand-shahar')),
('33333333-3333-3333-3333-333333333333', '+998971112233', 'Dilshod PetLover', 'user', TRUE, 1, (SELECT id FROM districts WHERE slug = 'chilonzor')),
('44444444-4444-4444-4444-444444444444', '+998998884422', 'Jasur Otboqar', 'user', TRUE, 2, (SELECT id FROM districts WHERE slug = 'bostonliq'))
ON CONFLICT (id) DO NOTHING;

-- ==============================================================================
-- 6. DEMO E'LONLAR (XILMA-XIL VA REAL MA'LUMOTLAR)
-- ==============================================================================

-- 1. Goloshtin sigir (Chorva)
INSERT INTO listings (
    id, seller_id, category_id, district_id,
    title, slug, description,
    price, currency, price_type,
    breed, gender, age_months, is_vaccinated, has_pedigree,
    attributes, contact_phone, is_vip, is_top, status
) VALUES (
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    '22222222-2222-2222-2222-222222222222',
    (SELECT id FROM categories WHERE slug = 'qoramol'),
    (SELECT id FROM districts WHERE slug = 'samarqand-shahar'),
    'Goloshtin zotli 1-qorin sog''in sigir, kuniga 26 litr sut beradi',
    'goloshtin-zotli-sogin-sigir-26-litr-sut',
    'Toza qonli Goloshtin zotli sigir sotiladi. Birinchi qorin tuqqan, sog''lom, xotirjam fe''l-atvorli. Barcha veterinariya emlashlari qilingan. Real xaridorga tushib beramiz.',
    28000000.00, 'UZS', 'negotiable',
    'Goloshtin-friz', 'female', 30, TRUE, TRUE,
    '{"daily_milk_liters": 26, "pregnancy_status": "tug''gan", "calving_count": 1, "weight_kg": 520}'::jsonb,
    '+998935557799', TRUE, TRUE, 'active'
) ON CONFLICT (id) DO NOTHING;

-- 2. Alabay kuchukchalari (Uy hayvonlari)
INSERT INTO listings (
    id, seller_id, category_id, district_id,
    title, slug, description,
    price, currency, price_type,
    breed, gender, age_months, is_vaccinated, has_pedigree,
    attributes, contact_phone, is_vip, is_top, status
) VALUES (
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    '33333333-3333-3333-3333-333333333333',
    (SELECT id FROM categories WHERE slug = 'itlar'),
    (SELECT id FROM districts WHERE slug = 'chilonzor'),
    'Toza qonli Oq Alabay (Bo''ribosar) kuchukchalari, pasporti bor',
    'toza-qonli-oq-alabay-boribosar-kuchukchalari',
    '2 oylik Alabay bolalari. Suyagi baquvvat, nasli toza chempion itlarning avlodi. 1-emlashi (Nobivac) qilingan, xalqaro veterinariya pasporti beriladi. 3 ta nar, 2 ta moya qoldi.',
    3500000.00, 'UZS', 'fixed',
    'Alabay (Bo''ribosar)', 'male', 2, TRUE, TRUE,
    '{"puppy_count": 5, "vaccine_name": "Nobivac Puppy DP", "color": "Oq-sariq"}'::jsonb,
    '+998971112233', TRUE, FALSE, 'active'
) ON CONFLICT (id) DO NOTHING;

-- 3. Hisori qo'chqor (Chorva)
INSERT INTO listings (
    id, seller_id, category_id, district_id,
    title, slug, description,
    price, currency, price_type,
    breed, gender, age_months, is_vaccinated, has_pedigree,
    attributes, contact_phone, is_vip, is_top, status
) VALUES (
    'cccccccc-cccc-cccc-cccc-cccccccccccc',
    '22222222-2222-2222-2222-222222222222',
    (SELECT id FROM categories WHERE slug = 'qoy-echki'),
    (SELECT id FROM districts WHERE slug = 'urgut'),
    'Boqilgan nasldor Hisori qo''chqor, 95 kg tirik vaznda',
    'boqilgan-nasldor-hisori-qochqor-95-kg',
    'Toza Hisori zotli semiz qo''chqor. Naslchilikka yoki to''y/ehson marosimlariga tayyor, toza makkajo''xori va bedada boqilgan.',
    5800000.00, 'UZS', 'negotiable',
    'Hisori', 'male', 18, TRUE, FALSE,
    '{"live_weight_kg": 95, "purpose": "Naslchilik / Go''sht"}'::jsonb,
    '+998935557799', FALSE, TRUE, 'active'
) ON CONFLICT (id) DO NOTHING;

-- 4. Qorabayir zotli to'riq uloqchi ot (Otlar)
INSERT INTO listings (
    id, seller_id, category_id, district_id,
    title, slug, description,
    price, currency, price_type,
    breed, gender, age_months, is_vaccinated, has_pedigree,
    attributes, contact_phone, is_vip, is_top, status
) VALUES (
    'dddddddd-dddd-dddd-dddd-dddddddddddd',
    '44444444-4444-4444-4444-444444444444',
    (SELECT id FROM categories WHERE slug = 'otlar'),
    (SELECT id FROM districts WHERE slug = 'bostonliq'),
    'Ko''pkari (Uloq) uchun tayyor 5 yoshli Qorabayir to''riq ayg''ir',
    'kopkari-uchun-5-yoshli-qorabayir-aygir',
    'Kopkari uloqlarida tajriba ko''rgan, baquvvat, quloqli va chopqir Qorabayir zotli to''riq ot. Barcha hujjatlari joyida, sog''lom, tuyoqlari mustahkam.',
    45000000.00, 'UZS', 'negotiable',
    'Qorabayir', 'male', 60, TRUE, TRUE,
    '{"suit": "To''riq", "withers_height_cm": 162, "sport_type": "Ko''pkari / Uloq"}'::jsonb,
    '+998998884422', TRUE, TRUE, 'active'
) ON CONFLICT (id) DO NOTHING;

-- 5. Shotland bukla quloq (Scottish Fold) mushukchalar
INSERT INTO listings (
    id, seller_id, category_id, district_id,
    title, slug, description,
    price, currency, price_type,
    breed, gender, age_months, is_vaccinated, has_pedigree,
    attributes, contact_phone, is_vip, is_top, status
) VALUES (
    'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
    '33333333-3333-3333-3333-333333333333',
    (SELECT id FROM categories WHERE slug = 'mushuklar'),
    (SELECT id FROM districts WHERE slug = 'yunusobod'),
    'Shotland vislouxim (Scottish Fold) moviy rangli yoqimtoy mushukcha',
    'shotland-vislouxim-moviy-rangli-mushukcha',
    '1.5 oylik go''zal zotli mushukcha. Lotokka (qumga) o''rgatilgan, o''zi mustaqil ovqatlana oladi. Juda erka va o''yinqaroq.',
    1200000.00, 'UZS', 'fixed',
    'Scottish Fold', 'female', 1, FALSE, FALSE,
    '{"fur_color": "Moviy kulrang (Blue)", "litter_trained": true}'::jsonb,
    '+998971112233', FALSE, FALSE, 'active'
) ON CONFLICT (id) DO NOTHING;

-- E'lon rasmlari
INSERT INTO listing_images (listing_id, image_url, is_primary, sort_order) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'https://images.unsplash.com/photo-1546445317-29f4545e9d53', TRUE, 1),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'https://images.unsplash.com/photo-1587300003388-59208cc962cb', TRUE, 1),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'https://images.unsplash.com/photo-1484557052118-f32bd25b45b5', TRUE, 1),
('dddddddd-dddd-dddd-dddd-dddddddddddd', 'https://images.unsplash.com/photo-1553284965-83fd3e82fa5a', TRUE, 1),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba', TRUE, 1)
ON CONFLICT DO NOTHING;

-- Demo Chat xabarlari
INSERT INTO conversations (id, listing_id, buyer_id, seller_id, last_message_text) VALUES
(
    '99999999-9999-9999-9999-999999999999',
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    '22222222-2222-2222-2222-222222222222', -- Xaridor: Alisher
    '33333333-3333-3333-3333-333333333333', -- Sotuvchi: Dilshod
    'Assalomu alaykum! Kuchukchalardan erkagi qoldimi?'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO messages (conversation_id, sender_id, content, is_read) VALUES
('99999999-9999-9999-9999-999999999999', '22222222-2222-2222-2222-222222222222', 'Assalomu alaykum! Kuchukchalardan erkagi qoldimi?', TRUE),
('99999999-9999-9999-9999-999999999999', '33333333-3333-3333-3333-333333333333', 'Vaalaykum assalom! Ha, 3 ta oq erkak kuchukcha bor, kelib ko''rishingiz mumkin.', FALSE);
