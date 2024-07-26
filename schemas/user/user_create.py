from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,  # 최소 길이 8자
        description="Password must be at least 8 characters long"
    )
    name: str
    age: int
    gender: str
    job: str
    category: str