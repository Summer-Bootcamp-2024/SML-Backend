from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    job: Optional[str] = None
    gender: Optional[str] = None
    company: Optional[str] = None
    region: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None