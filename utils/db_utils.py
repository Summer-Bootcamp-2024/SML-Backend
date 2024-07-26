from typing import List

from boto3 import session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schemas import UserSearchResult

async def get_users_from_db() -> List[UserSearchResult]:
    from ..models.user import User
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
