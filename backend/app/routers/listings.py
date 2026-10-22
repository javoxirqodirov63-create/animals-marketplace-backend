from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
import uuid
import json
from app.database import get_db, parse_json_safely
from app.schemas.listing import ListingListItem, ListingDetail, ListingCreate

router = APIRouter(prefix="/listings", tags=["E'lonlar (Listings)"])

@router.get("", response_model=List[ListingListItem], summary="E'lonlar lentasi (Filtrlar va qidiruv bilan)")
def list_listings(
    q: Optional[str] = Query(None, description="Qidiruv so'zi"),
    category_id: Optional[int] = Query(None, description="Kategoriya ID"),
    region_id: Optional[int] = Query(None, description="Viloyat ID"),
    district_id: Optional[int] = Query(None, description="Tuman ID"),
    min_price: Optional[float] = Query(None, description="Minimal narx"),
    max_price: Optional[float] = Query(None, description="Maksimal narx"),
    is_vip: Optional[bool] = Query(None, description="Faqat VIP e'lonlar"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    with get_db() as db:
        sql = """
        SELECT 
            l.id, l.title, l.slug, l.description, l.price, l.currency, l.price_type, l.breed,
            l.gender, l.age_months, l.is_vaccinated, l.has_pedigree,
            l.category_id, c.name_uz AS category_name,
            d.region_id, r.name_uz AS region_name,
            l.district_id, d.name_uz AS district_name,
            l.contact_phone, u.full_name AS seller_name,
            l.is_vip, l.is_top, l.views_count, l.favorites_count,
            (SELECT image_url FROM listing_images WHERE listing_id = l.id ORDER BY is_primary DESC, sort_order ASC LIMIT 1) AS primary_image_url,
            l.created_at
        FROM listings l
        JOIN categories c ON l.category_id = c.id
        JOIN districts d ON l.district_id = d.id
        JOIN regions r ON d.region_id = r.id
        JOIN users u ON l.seller_id = u.id
        WHERE l.status = 'active'
        """
        params = []
        
        if q:
            sql += " AND (l.title LIKE ? OR l.description LIKE ?)"
            params.extend([f"%{q}%", f"%{q}%"])
            
        if category_id:
            sql += " AND (l.category_id = ? OR c.parent_id = ?)"
            params.extend([category_id, category_id])
            
        if region_id:
            sql += " AND d.region_id = ?"
            params.append(region_id)
            
        if district_id:
            sql += " AND l.district_id = ?"
            params.append(district_id)
            
        if min_price is not None:
            sql += " AND l.price >= ?"
            params.append(min_price)
            
        if max_price is not None:
            sql += " AND l.price <= ?"
            params.append(max_price)
            
        if is_vip is not None:
            sql += " AND l.is_vip = ?"
            params.append(1 if is_vip else 0)
            
        sql += " ORDER BY l.is_vip DESC, l.is_top DESC, l.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        db.execute(sql, params)
        rows = db.fetchall()
        
        result = []
        for r in rows:
            primary_img = r["primary_image_url"] or "https://images.unsplash.com/photo-1546445317-29f4545e9d53"
            img_list = [primary_img]
            age_str = f"{r['age_months']} oylik" if r["age_months"] else ""
            gender_str = "Erkak" if r["gender"] == "male" else "Urg'ochi"
            
            result.append(ListingListItem(
                id=str(r["id"]),
                title=r["title"],
                slug=r["slug"],
                description=r["description"] or "",
                price=float(r["price"] or 0.0),
                currency=r["currency"] or "UZS",
                price_type=r["price_type"] or "fixed",
                is_negotiable=(r["price_type"] == "negotiable"),
                breed=r["breed"] or "",
                age=age_str,
                gender=gender_str,
                is_vaccinated=bool(r["is_vaccinated"]),
                has_passport=bool(r["has_pedigree"]),
                is_featured=bool(r["is_vip"] or r["is_top"]),
                is_verified_seller=True,
                category_id=r["category_id"],
                category_name=r["category_name"],
                region_id=r["region_id"],
                region_name=r["region_name"],
                district_id=r["district_id"],
                district_name=r["district_name"],
                contact_phone=r["contact_phone"] or "",
                seller_name=r["seller_name"] or "Foydalanuvchi",
                is_vip=bool(r["is_vip"]),
                is_top=bool(r["is_top"]),
                views_count=r["views_count"] or 0,
                favorites_count=r["favorites_count"] or 0,
                primary_image_url=primary_img,
                image_urls=img_list,
                created_at=str(r["created_at"])
            ))
        return result

@router.get("/{listing_id}", response_model=ListingDetail, summary="E'lonning to'liq ma'lumotlari")
def get_listing_detail(listing_id: str):
    with get_db() as db:
        db.execute("UPDATE listings SET views_count = views_count + 1 WHERE id = ?", (listing_id,))
        
        sql = """
        SELECT 
            l.id, l.seller_id, l.title, l.slug, l.description, l.price, l.currency,
            l.price_type, l.breed, l.gender, l.age_months, l.is_vaccinated, l.has_pedigree,
            l.attributes, l.contact_phone, l.is_vip, l.is_top, l.views_count, l.favorites_count,
            l.created_at,
            c.id AS category_id, c.name_uz AS category_name,
            d.region_id, r.name_uz AS region_name,
            d.id AS district_id, d.name_uz AS district_name,
            u.full_name AS seller_name,
            u.phone_number AS seller_phone
        FROM listings l
        JOIN categories c ON l.category_id = c.id
        JOIN districts d ON l.district_id = d.id
        JOIN regions r ON d.region_id = r.id
        JOIN users u ON l.seller_id = u.id
        WHERE l.id = ?
        """
        db.execute(sql, (listing_id,))
        item = db.fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="E'lon topilmadi")
            
        db.execute("SELECT image_url FROM listing_images WHERE listing_id = ? ORDER BY is_primary DESC, sort_order ASC", (listing_id,))
        img_rows = db.fetchall()
        images = [img["image_url"] for img in img_rows]
        if not images:
            images = ["https://images.unsplash.com/photo-1546445317-29f4545e9d53"]
        
        attrs = parse_json_safely(item["attributes"])
        age_str = f"{item['age_months']} oylik" if item["age_months"] else ""
        gender_str = "Erkak" if item["gender"] == "male" else "Urg'ochi"
        
        return ListingDetail(
            id=item["id"],
            title=item["title"],
            slug=item["slug"],
            description=item["description"],
            price=item["price"],
            currency=item["currency"],
            price_type=item["price_type"],
            is_negotiable=(item["price_type"] == "negotiable"),
            breed=item["breed"] or "",
            age=age_str,
            age_months=item["age_months"],
            gender=gender_str,
            is_vaccinated=bool(item["is_vaccinated"]),
            has_pedigree=bool(item["has_pedigree"]),
            has_passport=bool(item["has_pedigree"]),
            is_featured=bool(item["is_vip"] or item["is_top"]),
            is_verified_seller=True,
            attributes=attrs,
            contact_phone=item["contact_phone"] or "",
            category_id=item["category_id"],
            category_name=item["category_name"],
            region_id=item["region_id"],
            region_name=item["region_name"],
            district_id=item["district_id"],
            district_name=item["district_name"],
            is_vip=bool(item["is_vip"]),
            is_top=bool(item["is_top"]),
            views_count=item["views_count"],
            favorites_count=item["favorites_count"],
            primary_image_url=images[0],
            images=images,
            image_urls=images,
            seller_id=item["seller_id"],
            seller_name=item["seller_name"],
            seller_phone=item["seller_phone"],
            created_at=str(item["created_at"])
        )

@router.post("", response_model=ListingDetail, status_code=status.HTTP_201_CREATED, summary="Yangi e'lon joylash")
def create_listing(body: ListingCreate, seller_id: Optional[str] = Query("usr-alisher", description="Sotuvchi user ID")):
    new_id = str(uuid.uuid4())
    slug_val = body.title.lower().replace(" ", "-")[:50]
    
    with get_db() as db:
        sql = """
        INSERT INTO listings (
            id, seller_id, category_id, district_id, title, slug, description,
            price, currency, price_type, breed, gender, age_months, is_vaccinated,
            has_pedigree, attributes, contact_phone, status, is_vip, is_top
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', 0, 0)
        """
        db.execute(sql, (
            new_id,
            seller_id,
            body.category_id,
            body.district_id,
            body.title,
            slug_val,
            body.description,
            body.price,
            body.currency,
            body.price_type,
            body.breed,
            body.gender,
            body.age_months,
            1 if body.is_vaccinated else 0,
            1 if body.has_pedigree else 0,
            json.dumps(body.attributes),
            body.contact_phone
        ))
        
        for idx, url in enumerate(body.image_urls):
            db.execute(
                "INSERT INTO listing_images (listing_id, image_url, is_primary, sort_order) VALUES (?, ?, ?, ?)",
                (new_id, url, 1 if idx == 0 else 0, idx)
            )
            
    return get_listing_detail(new_id)

@router.post("/{listing_id}/favorite", summary="E'lonni sevimlilarga qo'shish / o'chirish (Toggle)")
def toggle_favorite(listing_id: str, user_id: str = Query("usr-dilshod")):
    with get_db() as db:
        db.execute("SELECT id FROM favorites WHERE user_id = ? AND listing_id = ?", (user_id, listing_id))
        fav = db.fetchone()
        
        if fav:
            db.execute("DELETE FROM favorites WHERE id = ?", (fav["id"],))
            is_fav = False
            msg = "E'lon sevimlilardan o'chirildi"
        else:
            db.execute("INSERT INTO favorites (user_id, listing_id) VALUES (?, ?)", (user_id, listing_id))
            is_fav = True
            msg = "E'lon sevimlilarga qo'shildi"
            
        db.execute("SELECT favorites_count FROM listings WHERE id = ?", (listing_id,))
        count_row = db.fetchone()
        count = count_row["favorites_count"] if count_row else 0
        
        return {"is_favorite": is_fav, "message": msg, "favorites_count": count}
