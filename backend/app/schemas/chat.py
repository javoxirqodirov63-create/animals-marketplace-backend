from pydantic import BaseModel, Field
from typing import Optional

class SendMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    listing_id: Optional[str] = None
    recipient_id: str
    sender_id: str
    content: str = Field(..., min_length=1, example="Assalomu alaykum! Narxini yana kelishamizmi?")

class MessageItem(BaseModel):
    id: int
    conversation_id: str
    sender_id: str
    sender_name: Optional[str]
    content: str
    is_read: bool
    created_at: str

class ConversationItem(BaseModel):
    id: str
    listing_id: Optional[str]
    listing_title: Optional[str]
    other_user_id: str
    other_user_name: Optional[str]
    last_message_text: Optional[str]
