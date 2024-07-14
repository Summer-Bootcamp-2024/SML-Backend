from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatroomCreate(BaseModel):
    user1_id: int
    user2_id: int
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True