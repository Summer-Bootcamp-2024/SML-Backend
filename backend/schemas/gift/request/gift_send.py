from pydantic import BaseModel
from typing import Optional

class GiftSend(BaseModel):
    user_id: int
    friend_id: int
    ct_money: int
