from pydantic import BaseModel
from typing import Optional

class RegionResponse(BaseModel):
    id: int
    name_uz: str
    name_ru: str
    slug: str
    sort_order: int

class DistrictResponse(BaseModel):
    id: int
    region_id: int
    name_uz: str
    name_ru: str
    slug: str
    sort_order: Optional[int] = 0
