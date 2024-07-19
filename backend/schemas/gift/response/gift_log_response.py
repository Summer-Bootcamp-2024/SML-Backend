from typing import List
from pydantic import BaseModel
from Backend.backend.schemas.gift.response.gift_response import GiftResponse

class GiftResponseLog(BaseModel):
    transactions: List[GiftResponse]

    class Config:
        from_attributes = True


