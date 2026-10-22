from pydantic import BaseModel, Field
from typing import Optional

class SendOTPRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567")

class SendOTPResponse(BaseModel):
    success: bool
    message: str
    demo_code: Optional[str] = None  # Test muhitida darhol ko'rish uchun

class VerifyOTPRequest(BaseModel):
    phone_number: str = Field(..., example="+998901234567")
    code: str = Field(..., example="7777")
    full_name: Optional[str] = Field(None, example="Dilshod Karimov")

class UserProfile(BaseModel):
    id: str
    phone_number: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    role: str
    is_verified: bool

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
