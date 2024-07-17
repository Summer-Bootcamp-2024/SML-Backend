from datetime import datetime
from pydantic import BaseModel

class MessageCreate(BaseModel):
    room_id: int
    sender_id: int
    content: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    id: int
    room_id: int
    sender_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
