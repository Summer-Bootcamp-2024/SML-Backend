from typing import Optional

from pydantic import BaseModel

class FriendsFind(BaseModel):
    user_id: int
    friend_id: int
    status: Optional[str] = 'accepted'
    is_deleted: Optional[bool] = False

    class Config:
         orm_mode = True