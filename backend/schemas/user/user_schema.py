from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    region: str
    gender: str
    status: Optional[str] = None
    age: Optional[int] = None
    job: Optional[str] = None
    company: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    credit: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True