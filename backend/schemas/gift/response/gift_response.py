from typing import Optional

from pydantic import BaseModel
from datetime import datetime

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class GiftResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    ct_money: int
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        from_attributes = True

