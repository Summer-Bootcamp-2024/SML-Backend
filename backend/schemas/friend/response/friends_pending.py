from typing import Optional

from pydantic import BaseModel


class FriendPending(BaseModel):
    user_id: int
    friend_id: int
    status: Optional[str] = None