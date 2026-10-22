from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import uuid
from app.database import get_db
from app.schemas.chat import ConversationItem, MessageItem, SendMessageRequest

router = APIRouter(prefix="/chat", tags=["Ichki Chat (In-app Messaging)"])

@router.get("/conversations", response_model=List[ConversationItem], summary="Foydalanuvchining barcha chat suhbatlari")
def get_user_conversations(user_id: str = Query("usr-dilshod")):
    """Foydalanuvchi qatnashayotgan barcha chat xonalari ro'yxatini qaytaradi."""
    with get_db() as db:
        sql = """
        SELECT 
            c.id, c.listing_id, c.last_message_text,
            l.title AS listing_title,
            CASE WHEN c.buyer_id = ? THEN c.seller_id ELSE c.buyer_id END AS other_user_id,
            u.full_name AS other_user_name
        FROM conversations c
        LEFT JOIN listings l ON c.listing_id = l.id
        JOIN users u ON u.id = (CASE WHEN c.buyer_id = ? THEN c.seller_id ELSE c.buyer_id END)
        WHERE c.buyer_id = ? OR c.seller_id = ?
        ORDER BY c.created_at DESC
        """
        db.execute(sql, (user_id, user_id, user_id, user_id))
        rows = db.fetchall()
        return [ConversationItem(**r) for r in rows]

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageItem], summary="Chatdagi xabarlar tarixi")
def get_messages(conversation_id: str):
    """Bitta suhbatdagi barcha xabarlarni vaqt tartibida qaytaradi."""
    with get_db() as db:
        # Xabarlarni o'qilgan qilib belgilash
        db.execute("UPDATE messages SET is_read = 1 WHERE conversation_id = ?", (conversation_id,))
        
        sql = """
        SELECT m.id, m.conversation_id, m.sender_id, m.content, m.is_read, m.created_at, u.full_name AS sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.conversation_id = ?
        ORDER BY m.created_at ASC
        """
        db.execute(sql, (conversation_id,))
        rows = db.fetchall()
        return [MessageItem(**{**r, "is_read": bool(r["is_read"]), "created_at": str(r["created_at"])}) for r in rows]

@router.post("/messages", response_model=MessageItem, summary="Yangi xabar yuborish")
def send_message(body: SendMessageRequest):
    """
    Sotuvchiga yoki xaridorga xabar yuboradi.
    Agar suhbat mavjud bo'lmasa, yangi suhbat xonasi ochiladi.
    """
    with get_db() as db:
        conv_id = body.conversation_id
        
        if not conv_id:
            # Suhbat xonasini qidirish yoki yaratish
            sql_find = """
            SELECT id FROM conversations 
            WHERE listing_id = ? AND ((buyer_id = ? AND seller_id = ?) OR (buyer_id = ? AND seller_id = ?))
            """
            db.execute(sql_find, (body.listing_id, body.sender_id, body.recipient_id, body.recipient_id, body.sender_id))
            row = db.fetchone()
            
            if row:
                conv_id = row["id"]
            else:
                conv_id = str(uuid.uuid4())
                db.execute(
                    "INSERT INTO conversations (id, listing_id, buyer_id, seller_id, last_message_text) VALUES (?, ?, ?, ?, ?)",
                    (conv_id, body.listing_id, body.sender_id, body.recipient_id, body.content)
                )
        else:
            # Oxirgi xabar matnini yangilash
            db.execute("UPDATE conversations SET last_message_text = ? WHERE id = ?", (body.content, conv_id))
            
        # Xabarni yozish
        db.execute(
            "INSERT INTO messages (conversation_id, sender_id, content, is_read) VALUES (?, ?, ?, 0)",
            (conv_id, body.sender_id, body.content)
        )
        msg_id = db.lastrowid
        
        db.execute("SELECT full_name FROM users WHERE id = ?", (body.sender_id,))
        user_row = db.fetchone()
        sender_name = user_row["full_name"] if user_row else "Foydalanuvchi"
        
        return MessageItem(
            id=msg_id,
            conversation_id=conv_id,
            sender_id=body.sender_id,
            sender_name=sender_name,
            content=body.content,
            is_read=False,
            created_at="hozir"
        )
