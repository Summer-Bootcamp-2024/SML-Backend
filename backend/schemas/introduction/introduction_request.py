from typing import Optional

from pydantic import BaseModel
from datetime import datetime

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class IntroductionRequestBase(BaseModel):
    user_id: int
    target_user_id: int
    intermediary_user_id: int

class IntroductionRequestCreate(IntroductionRequestBase):
    pass

class IntroductionRequestUpdate(BaseModel):
    status: str

class IntroductionRequest(IntroductionRequestBase):
    id: int
    status: str
    created_at: Optional[datetime] = formatted_timestamp
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True
