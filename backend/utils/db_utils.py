from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.schemas.search.search_schema import UserSearchResult
from Backend.backend.database import async_session
from Backend.backend.models.user import User  # User 모델을 올바르게 임포트

async def get_users_from_db() -> List[UserSearchResult]:
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()

    return [UserSearchResult(
        id=user.id,
        name=user.name,
        region=user.region,
        gender=user.gender,
        age=user.age,
        job=user.job,
        company=user.company,
        category=user.category,
        image_url=user.image_url)
        for user in users]
