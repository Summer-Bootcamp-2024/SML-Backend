from pydantic import BaseModel
from datetime import datetime

class CreditUpdate(BaseModel):
    credits: int

class CreditResponse(BaseModel):
    id: int
    credit: int
    updated_at: datetime

    class Config:
        from_attributes = True
