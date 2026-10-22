from fastapi import APIRouter
from typing import List
from app.database import get_db
from app.schemas.category import CategoryTree, CategoryChild

router = APIRouter(prefix="/categories", tags=["Kategoriyalar"])

@router.get("", response_model=List[CategoryTree], summary="Ierarxik kategoriyalar daraxtini olish")
def get_categories_tree():
    """Bosh kategoriyalar va ularning ichidagi barcha ost-kategoriyalarni bitta daraxt ko'rinishida qaytaradi."""
    with get_db() as db:
        # Bosh toifalar
        db.execute("SELECT id, name_uz, name_ru, slug, sort_order FROM categories WHERE parent_id IS NULL ORDER BY sort_order ASC, id ASC")
        parents = db.fetchall()
        
        # Ost toifalar
        db.execute("SELECT id, parent_id, name_uz, name_ru, slug, sort_order FROM categories WHERE parent_id IS NOT NULL ORDER BY sort_order ASC, id ASC")
        children = db.fetchall()
        
        result = []
        for p in parents:
            p_children = [CategoryChild(**c) for c in children if c["parent_id"] == p["id"]]
            result.append(CategoryTree(
                id=p["id"],
                name_uz=p["name_uz"],
                name_ru=p["name_ru"],
                slug=p["slug"],
                sort_order=p["sort_order"],
                subcategories=p_children
            ))
        return result
