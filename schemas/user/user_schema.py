from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from Backend.utils.s3_util import default_profile_url

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class User(BaseModel):
    id: int
    name: str
    gender: str
    age: int
    job: str
    category: str
    region: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    image_url: Optional[str] = default_profile_url
    credit: Optional[int] = None
    created_at: Optional[datetime] = formatted_timestamp
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        orm_mode = True