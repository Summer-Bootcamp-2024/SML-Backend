from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from Backend.backend.utils.s3_util import default_profile_url

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
    image_url: Optional[str] = default_profile_url
    credit: Optional[int] = None
    created_at: Optional[datetime] = formatted_timestamp
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True