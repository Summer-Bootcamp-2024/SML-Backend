from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import User
async def update_credit(db: AsyncSession, user_id: int, credits: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if user:
        user.credit += credits
        await db.commit()
        await db.refresh(user)

    return user
