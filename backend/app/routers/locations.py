from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.database import get_db
from app.schemas.location import RegionResponse, DistrictResponse

router = APIRouter(prefix="/locations", tags=["Hududlar va Lokatsiya"])

@router.get("/regions", response_model=List[RegionResponse], summary="Barcha viloyatlar ro'yxatini olish")
def get_regions():
    """O'zbekistonning barcha 14 ta hududini tartiblangan holda qaytaradi."""
    with get_db() as db:
        db.execute("SELECT id, name_uz, name_ru, slug, sort_order FROM regions ORDER BY sort_order ASC, id ASC")
        return db.fetchall()

@router.get("/districts", response_model=List[DistrictResponse], summary="Tumanlar va shaharlar ro'yxati")
def get_districts(region_id: Optional[int] = Query(None, description="Viloyat ID raqami bo'yicha filtrlash")):
    """Berilgan viloyatga tegishli tumanlar yoki barcha tumanlar ro'yxatini qaytaradi."""
    with get_db() as db:
        if region_id is not None:
            db.execute(
                "SELECT id, region_id, name_uz, name_ru, slug, sort_order FROM districts WHERE region_id = ? ORDER BY sort_order ASC, name_uz ASC",
                (region_id,)
            )
        else:
            db.execute("SELECT id, region_id, name_uz, name_ru, slug, sort_order FROM districts ORDER BY region_id ASC, name_uz ASC")
        return db.fetchall()
