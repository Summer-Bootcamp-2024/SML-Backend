from pydantic import BaseModel
from datetime import datetime

class GiftResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    ct_money: int
    updated_at: datetime

    class Config:
        orm_mode = True