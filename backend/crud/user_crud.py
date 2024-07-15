from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Backend.backend.models.user import User
from Backend.backend.schemas.user.user_create import UserCreate
from Backend.backend.schemas.user.user_update import UserUpdate

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        email=user.email,
        password=user.password,  # 비밀번호를 해시화하는 것이 좋습니다
        name=user.name,
        region=user.region,
        gender=user.gender
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
