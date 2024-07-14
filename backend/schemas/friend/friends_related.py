from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class FriendsFind(BaseModel):
    user_id: int
    friend_id: int
    is_deleted: Optional[bool] = False

    class Config:
         orm_mode = True