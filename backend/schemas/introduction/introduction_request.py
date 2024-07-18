from typing import Optional

from pydantic import BaseModel
from datetime import datetime

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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
