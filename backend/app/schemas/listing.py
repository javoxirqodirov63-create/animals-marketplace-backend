from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ListingListItem(BaseModel):
    id: str
    title: str
    slug: Optional[str] = None
    description: Optional[str] = ""
    price: float
    currency: str = "UZS"
    price_type: str = "fixed"
    is_negotiable: bool = True
    breed: Optional[str] = None
    age: Optional[str] = ""
    gender: Optional[str] = "Erkak"
    is_vaccinated: bool = True
    has_passport: bool = True
    is_featured: bool = False
    is_verified_seller: bool = True
    category_id: Optional[int] = 1
    category_name: str
    region_id: Optional[int] = 1
    region_name: str
    district_id: Optional[int] = 1
    district_name: str
    contact_phone: Optional[str] = ""
    seller_name: Optional[str] = "Foydalanuvchi"
    is_vip: bool = False
    is_top: bool = False
    views_count: int = 0
    favorites_count: int = 0
    primary_image_url: Optional[str] = None
    image_urls: List[str] = []
    created_at: str

class ListingDetail(ListingListItem):
    age_months: Optional[int] = None
    has_pedigree: bool = False
    attributes: Dict[str, Any] = {}
    seller_id: Optional[str] = None
    seller_phone: Optional[str] = None
    images: List[str] = []

class ListingCreate(BaseModel):
    category_id: int
    district_id: int
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field("", min_length=0)
    price: float = Field(0.0, ge=0)
    currency: str = Field("UZS")
    price_type: str = Field("negotiable")
    breed: Optional[str] = None
    gender: Optional[str] = "male"
    age_months: Optional[int] = 12
    is_vaccinated: bool = True
    has_pedigree: bool = False
    attributes: Dict[str, Any] = Field(default_factory=dict)
    contact_phone: str = Field("+998901234567")
    image_urls: List[str] = Field(default_factory=list)
