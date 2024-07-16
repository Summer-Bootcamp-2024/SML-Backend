from typing import Optional
from pydantic import BaseModel

class UserSearchResult(BaseModel):
    id: int
    name: str
    region: str
    gender: str
    age: Optional[int] = None
    job: Optional[str] = None
    company: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class SearchFilters(BaseModel):
    user_id: int
    search: str