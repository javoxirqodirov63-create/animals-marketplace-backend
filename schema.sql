-- ==============================================================================
-- Universal Hayvonlar Bozori (Pet & Livestock Marketplace)
-- PostgreSQL Database Schema
-- Versiya: 1.1.0 (Optimallashtirilgan va to'liq himoyalangan)
-- ==============================================================================

-- Kengaytmalar (Extensions)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ==============================================================================
-- ENUM TURLARI
-- ==============================================================================

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('user', 'moderator', 'admin');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE listing_status AS ENUM ('active', 'sold', 'archived', 'blocked');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE price_type AS ENUM ('fixed', 'negotiable', 'free');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE currency_code AS ENUM ('UZS', 'USD');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE animal_gender AS ENUM ('male', 'female', 'unknown');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE message_type AS ENUM ('text', 'image', 'audio');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE report_reason AS ENUM (
        'prohibited_animal',    -- Qizil kitob / taqiqlangan yovvoyi hayvon
        'scam_fraud',           -- Firibgarlik / soxta e'lon
        'wrong_price',          -- Noto'g'ri ko'rsatilgan narx
        'cruelty_abuse',        -- Hayvonlarga shafqatsiz munosabat
        'duplicate_spam',       -- Dublikat / spam
        'other'                 -- Boshqa sabab
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE report_status AS ENUM ('pending', 'resolved', 'dismissed');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE promotion_type AS ENUM ('vip', 'top', 'urgent');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE payment_provider AS ENUM ('click', 'payme', 'uzum', 'manual');
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE payment_status AS ENUM ('pending', 'completed', 'failed', 'refunded');
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- ==============================================================================
-- 1. HUDUDLAR (GEOGRAFIYA) JADVALLARI
-- ==============================================================================

-- Viloyatlar (14 ta ma'muriy hudud)
CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    name_uz VARCHAR(100) NOT NULL,
    name_ru VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tumanlar va shaharlar
CREATE TABLE IF NOT EXISTS districts (
    id SERIAL PRIMARY KEY,
    region_id INT NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    name_uz VARCHAR(100) NOT NULL,
    name_ru VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_region_district_slug UNIQUE (region_id, slug)
);

-- ==============================================================================
-- 2. FOYDALANUVCHILAR VA XAVFSIZLIK JADVALLARI
-- ==============================================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(120),
    avatar_url TEXT,
    bio TEXT,
    telegram_username VARCHAR(50),
    region_id INT REFERENCES regions(id) ON DELETE SET NULL,
    district_id INT REFERENCES districts(id) ON DELETE SET NULL,
    role user_role DEFAULT 'user',
    is_verified BOOLEAN DEFAULT FALSE,
    is_blocked BOOLEAN DEFAULT FALSE,
    blocked_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT chk_user_phone CHECK (length(phone_number) >= 9)
);

-- SMS orqali tasdiqlash kodlari (OTP)
CREATE TABLE IF NOT EXISTS otp_codes (
    id BIGSERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    code_hash VARCHAR(255) NOT NULL,
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 5,
    expires_at TIMESTAMPTZ NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 3. KATEGORIYALAR (IERARXIK DARAХT)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    parent_id INT REFERENCES categories(id) ON DELETE CASCADE,
    name_uz VARCHAR(100) NOT NULL,
    name_ru VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    icon_url TEXT,
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 4. E'LONLAR VA RASMLAR (LISTINGS & IMAGES)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS listings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    seller_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    district_id INT NOT NULL REFERENCES districts(id) ON DELETE RESTRICT,
    
    -- E'lon asosiy ma'lumotlari
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(250),
    description TEXT NOT NULL,
    price NUMERIC(14, 2) DEFAULT 0.00 CHECK (price >= 0),
    currency currency_code DEFAULT 'UZS',
    price_type price_type DEFAULT 'fixed',
    
    -- Hayvonning xarakteristikalari
    breed VARCHAR(100),                          -- Zoti (masalan: Alabay, Shotland, Goloshtin)
    gender animal_gender DEFAULT 'unknown',      -- Jinsi
    age_months INT CHECK (age_months >= 0),      -- Yoshi (oylarda)
    is_vaccinated BOOLEAN DEFAULT FALSE,         -- Emlanganmi
    has_pedigree BOOLEAN DEFAULT FALSE,          -- Pasport / zotdorlik hujjati bormi
    
    -- Moslashuvchan qo'shimcha parametrlar (JSONB)
    attributes JSONB DEFAULT '{}'::jsonb,
    
    -- Aloqa sozlamalari
    contact_phone VARCHAR(20) NOT NULL,
    allow_inapp_chat BOOLEAN DEFAULT TRUE,
    show_telegram BOOLEAN DEFAULT FALSE,
    
    -- Status va ko'rsatkichlar
    status listing_status DEFAULT 'active',
    views_count INT DEFAULT 0 CHECK (views_count >= 0),
    favorites_count INT DEFAULT 0 CHECK (favorites_count >= 0),
    
    -- Reklama va TOP ko'rsatkichlar
    is_vip BOOLEAN DEFAULT FALSE,
    is_top BOOLEAN DEFAULT FALSE,
    is_urgent BOOLEAN DEFAULT FALSE,
    promoted_until TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- E'lon rasmlari
CREATE TABLE IF NOT EXISTS listing_images (
    id BIGSERIAL PRIMARY KEY,
    listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Saqlangan e'lonlar (Sevimlilar / Favorites)
CREATE TABLE IF NOT EXISTS favorites (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_user_favorite_listing UNIQUE (user_id, listing_id)
);

-- ==============================================================================
-- 5. CHAT VA XABARLAR (IN-APP REAL-TIME CHAT)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    listing_id UUID REFERENCES listings(id) ON DELETE SET NULL,
    buyer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    seller_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    last_message_text TEXT,
    last_message_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_conversation_participants UNIQUE (listing_id, buyer_id, seller_id)
);

CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_type message_type DEFAULT 'text',
    content TEXT,
    attachment_url TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 6. MODERATSIYA VA SHIKOYATLAR (REPORTS)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS listing_reports (
    id BIGSERIAL PRIMARY KEY,
    listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    reporter_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reason report_reason NOT NULL,
    description TEXT,
    status report_status DEFAULT 'pending',
    admin_notes TEXT,
    reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

-- ==============================================================================
-- 7. MONETIZATSIYA VA TO'LOVLAR (PROMOTIONS & PAYMENTS)
-- ==============================================================================

-- VIP va TOP e'lon tariflari
CREATE TABLE IF NOT EXISTS promotion_plans (
    id SERIAL PRIMARY KEY,
    name_uz VARCHAR(100) NOT NULL,
    name_ru VARCHAR(100) NOT NULL,
    type promotion_type NOT NULL,
    duration_days INT NOT NULL CHECK (duration_days > 0),
    price_uzs NUMERIC(12, 2) NOT NULL CHECK (price_uzs >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- To'lov tranzaksiyalari (Click, Payme, Uzum)
CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    plan_id INT NOT NULL REFERENCES promotion_plans(id) ON DELETE RESTRICT,
    provider payment_provider NOT NULL,
    amount_uzs NUMERIC(12, 2) NOT NULL CHECK (amount_uzs >= 0),
    status payment_status DEFAULT 'pending',
    external_transaction_id VARCHAR(150),
    provider_payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================================================
-- 8. INDEKSLAR (TEZKOR QIDIRUV VA FILTRLAR UCHUN)
-- ==============================================================================

CREATE INDEX IF NOT EXISTS idx_listings_category_status ON listings(category_id, status);
CREATE INDEX IF NOT EXISTS idx_listings_district_status ON listings(district_id, status);
CREATE INDEX IF NOT EXISTS idx_listings_status ON listings(status);
CREATE INDEX IF NOT EXISTS idx_listings_price ON listings(price);
CREATE INDEX IF NOT EXISTS idx_listings_vip_created ON listings(is_vip DESC, is_top DESC, created_at DESC) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_listings_attributes_gin ON listings USING GIN (attributes);
CREATE INDEX IF NOT EXISTS idx_listings_title_trgm ON listings USING GIN (title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_listings_desc_trgm ON listings USING GIN (description gin_trgm_ops);

-- Chat va xabarlar indekslari
CREATE INDEX IF NOT EXISTS idx_messages_conversation_created ON messages(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_conversations_buyer ON conversations(buyer_id);
CREATE INDEX IF NOT EXISTS idx_conversations_seller ON conversations(seller_id);

-- Foydalanuvchilar va OTP indekslari
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone_number);
CREATE INDEX IF NOT EXISTS idx_otp_phone ON otp_codes(phone_number, expires_at);

-- ==============================================================================
-- 9. TRIGGERLAR VA FUNKSIYALAR
-- ==============================================================================

-- updated_at ustunini avtomatik yangilovchi universal funksiya
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_users_updated_at ON users;
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_listings_updated_at ON listings;
CREATE TRIGGER trg_listings_updated_at
BEFORE UPDATE ON listings
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_payments_updated_at ON payments;
CREATE TRIGGER trg_payments_updated_at
BEFORE UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

-- Sevimlilar sonini (favorites_count) avtomatik sinxron saqlovchi trigger
CREATE OR REPLACE FUNCTION update_listing_favorites_count()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE listings SET favorites_count = favorites_count + 1 WHERE id = NEW.listing_id;
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        UPDATE listings SET favorites_count = GREATEST(0, favorites_count - 1) WHERE id = OLD.listing_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_favorites_count_sync ON favorites;
CREATE TRIGGER trg_favorites_count_sync
AFTER INSERT OR DELETE ON favorites
FOR EACH ROW
EXECUTE FUNCTION update_listing_favorites_count();

-- ==============================================================================
-- 10. QULAY VIEW'LAR (FRONTEND VA BACKEND UCHUN TAYYOR KO'RINISHLAR)
-- ==============================================================================

-- Barcha faol e'lonlarni asosiy rasm va joylashuv ma'lumotlari bilan bitta so'rovda olish
CREATE OR REPLACE VIEW v_active_listings AS
SELECT 
    l.id,
    l.title,
    l.slug,
    l.description,
    l.price,
    l.currency,
    l.price_type,
    l.breed,
    l.gender,
    l.age_months,
    l.is_vaccinated,
    l.has_pedigree,
    l.attributes,
    l.is_vip,
    l.is_top,
    l.is_urgent,
    l.views_count,
    l.favorites_count,
    l.created_at,
    -- Kategoriya ma'lumotlari
    c.id AS category_id,
    c.name_uz AS category_name_uz,
    c.name_ru AS category_name_ru,
    c.slug AS category_slug,
    -- Joylashuv
    d.id AS district_id,
    d.name_uz AS district_name_uz,
    r.id AS region_id,
    r.name_uz AS region_name_uz,
    -- Sotuvchi
    u.id AS seller_id,
    u.full_name AS seller_name,
    u.phone_number AS seller_phone,
    u.telegram_username AS seller_telegram,
    -- Asosiy rasm
    COALESCE(
        (SELECT img.image_url FROM listing_images img WHERE img.listing_id = l.id AND img.is_primary = TRUE LIMIT 1),
        (SELECT img.image_url FROM listing_images img WHERE img.listing_id = l.id ORDER BY img.sort_order ASC, img.created_at ASC LIMIT 1)
    ) AS primary_image_url
FROM listings l
JOIN categories c ON l.category_id = c.id
JOIN districts d ON l.district_id = d.id
JOIN regions r ON d.region_id = r.id
JOIN users u ON l.seller_id = u.id
WHERE l.status = 'active';
