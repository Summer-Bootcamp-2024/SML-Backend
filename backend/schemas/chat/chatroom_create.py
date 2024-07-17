from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatroomCreate(BaseModel):
    user1_id: int
    user2_id: int
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()

    class Config:
        orm_mode = True

class ChatroomResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ChatroomResponse2(BaseModel):
    id: int
    user1_id: int
    user1_name: str
    user1_image_url: Optional[str]
    user2_id: int
    user2_name: str
    user2_image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True