from datetime import datetime
from typing import Optional

from pydantic import BaseModel

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class MessageCreate(BaseModel):
    room_id: int
    sender_id: int
    content: str
    timestamp: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    id: int
    room_id: int
    sender_id: int
    content: str
    timestamp: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True
