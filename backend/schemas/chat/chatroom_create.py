from datetime import datetime
from typing import Optional

from pydantic import BaseModel

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class ChatroomCreate(BaseModel):
    user1_id: int
    user2_id: int

    class Config:
        orm_mode = True

class ChatroomResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: Optional[datetime] = formatted_timestamp
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True

class ChatroomResponse2(BaseModel):
    id: int
    user1_id: int
    user1_name: str
    user1_image_url: Optional[str] = None
    user2_id: int
    user2_name: str
    user2_image_url: Optional[str] = None
    created_at: Optional[datetime] = formatted_timestamp
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True

class DeleteResponse(BaseModel):
    detail: str