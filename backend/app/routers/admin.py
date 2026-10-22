from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import List, Optional
from app.database import get_db

router = APIRouter(tags=["Admin Panel"])

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# 1. Admin Veb-Sahifasini uzatish (HTML)
@router.get("/admin", response_class=HTMLResponse, summary="Admin Panel Veb-Sahifasi")
def get_admin_page():
    html_file = TEMPLATES_DIR / "admin.html"
    if not html_file.exists():
        return HTMLResponse("<h1>Admin Panel fayli topilmadi</h1>", status_code=404)
    with open(html_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 2. Statistika ma'lumotlari
@router.get("/api/admin/stats", summary="Umumiy statistika")
def get_admin_stats():
    with get_db() as db:
        db.execute("SELECT COUNT(*) AS total FROM listings")
        total_listings = db.fetchone()["total"]

        db.execute("SELECT COUNT(*) AS total FROM listings WHERE status = 'active'")
        active_listings = db.fetchone()["total"]

        db.execute("SELECT COUNT(*) AS total FROM listings WHERE is_vip = 1")
        vip_listings = db.fetchone()["total"]

        db.execute("SELECT COUNT(*) AS total FROM users")
        total_users = db.fetchone()["total"]

        db.execute("SELECT COUNT(*) AS total FROM listing_reports WHERE status = 'pending'")
        pending_reports = db.fetchone()["total"]

        return {
            "total_listings": total_listings,
            "active_listings": active_listings,
            "vip_listings": vip_listings,
            "total_users": total_users,
            "pending_reports": pending_reports
        }

# 3. Barcha e'lonlar ro'yxati (Boshqaruv uchun)
@router.get("/api/admin/listings", summary="Barcha e'lonlar (Admin ko'rinishi)")
def get_all_listings_admin():
    with get_db() as db:
        sql = """
        SELECT 
            l.id, l.title, l.price, l.currency, l.price_type, l.breed, l.status,
            l.is_vip, l.is_top, l.views_count, l.favorites_count, l.created_at,
            c.name_uz AS category_name,
            r.name_uz AS region_name,
            d.name_uz AS district_name,
            u.full_name AS seller_name,
            u.phone_number AS seller_phone,
            (SELECT image_url FROM listing_images WHERE listing_id = l.id ORDER BY is_primary DESC LIMIT 1) AS image_url
        FROM listings l
        JOIN categories c ON l.category_id = c.id
        JOIN districts d ON l.district_id = d.id
        JOIN regions r ON d.region_id = r.id
        JOIN users u ON l.seller_id = u.id
        ORDER BY l.created_at DESC
        """
        db.execute(sql)
        return db.fetchall()

# 4. E'lon holatini o'zgartirish (Bloklash / Faollashtirish)
@router.patch("/api/admin/listings/{listing_id}/status", summary="E'lon statusini o'zgartirish")
def update_listing_status(listing_id: str, new_status: str = Query(..., regex="^(active|blocked|sold|archived)$")):
    with get_db() as db:
        db.execute("SELECT id FROM listings WHERE id = ?", (listing_id,))
        if not db.fetchone():
            raise HTTPException(status_code=404, detail="E'lon topilmadi")
        
        db.execute("UPDATE listings SET status = ? WHERE id = ?", (new_status, listing_id))
        return {"success": True, "message": f"E'lon statusi '{new_status}' ga o'zgartirildi", "listing_id": listing_id}

# 5. VIP statusini yoqish / o'chirish (Toggle VIP)
@router.patch("/api/admin/listings/{listing_id}/toggle-vip", summary="VIP statusini o'zgartirish")
def toggle_vip(listing_id: str):
    with get_db() as db:
        db.execute("SELECT is_vip FROM listings WHERE id = ?", (listing_id,))
        row = db.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="E'lon topilmadi")
        
        current_vip = bool(row["is_vip"])
        new_vip = 0 if current_vip else 1
        db.execute("UPDATE listings SET is_vip = ? WHERE id = ?", (new_vip, listing_id))
        
        msg = "E'lon VIP qilindi!" if new_vip else "VIP statusi bekor qilindi"
        return {"success": True, "is_vip": bool(new_vip), "message": msg}

# 6. E'lonni butunlay o'chirish
@router.delete("/api/admin/listings/{listing_id}", summary="E'lonni o'chirish")
def delete_listing_admin(listing_id: str):
    with get_db() as db:
        db.execute("SELECT id FROM listings WHERE id = ?", (listing_id,))
        if not db.fetchone():
            raise HTTPException(status_code=404, detail="E'lon topilmadi")
        
        db.execute("DELETE FROM listings WHERE id = ?", (listing_id,))
        return {"success": True, "message": "E'lon muvaffaqiyatli o'chirildi"}

# 7. Foydalanuvchilar ro'yxati
@router.get("/api/admin/users", summary="Barcha foydalanuvchilar")
def get_users_admin():
    with get_db() as db:
        sql = """
        SELECT 
            u.id, u.phone_number, u.full_name, u.role, u.is_verified,
            (SELECT COUNT(*) FROM listings WHERE seller_id = u.id) AS listings_count
        FROM users u
        ORDER BY u.created_at DESC
        """
        db.execute(sql)
        return db.fetchall()

# 8. Shikoyatlar ro'yxati
@router.get("/api/admin/reports", summary="Shikoyatlar ro'yxati")
def get_reports_admin():
    with get_db() as db:
        sql = """
        SELECT 
            r.id, r.listing_id, r.reason, r.status,
            l.title AS listing_title,
            u.full_name AS reporter_name,
            u.phone_number AS reporter_phone
        FROM listing_reports r
        JOIN listings l ON r.listing_id = l.id
        JOIN users u ON r.reporter_id = u.id
        ORDER BY r.id DESC
        """
        db.execute(sql)
        return db.fetchall()
