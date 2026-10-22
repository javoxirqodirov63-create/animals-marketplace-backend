from pydantic import BaseModel
from typing import Optional, List

class CategoryChild(BaseModel):
    id: int
    parent_id: Optional[int]
    name_uz: str
    name_ru: str
    slug: str
    sort_order: Optional[int] = 0

class CategoryTree(BaseModel):
    id: int
    name_uz: str
    name_ru: str
    slug: str
    sort_order: Optional[int] = 0
    subcategories: List[CategoryChild] = []
