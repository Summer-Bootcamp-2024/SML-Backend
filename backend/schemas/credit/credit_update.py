from typing import Optional

from pydantic import BaseModel
from datetime import datetime

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class CreditUpdate(BaseModel):
    credits: int

class CreditResponse(BaseModel):
    id: int
    credit: int
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        from_attributes = True
