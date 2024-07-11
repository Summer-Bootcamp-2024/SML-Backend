from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.models.user import User


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()