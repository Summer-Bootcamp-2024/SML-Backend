from sqlalchemy import delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Backend.backend.models.friends import Friend
from Backend.backend.models.user import User
from Backend.backend.schemas.search.search_schema import UserSearchResult
from Backend.backend.schemas.user.user_create import UserCreate
from Backend.backend.schemas.user.user_update import UserUpdate
from Backend.backend.utils.index_user import es


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

    user_data = UserSearchResult(id=db_user.id, email=db_user.email, name=db_user.name, region=db_user.region, gender=db_user.gender)
    es.index(index="users", id=db_user.id, body=user_data.dict())

    return db_user

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)

        user_data = UserSearchResult(id=db_user.id, email=db_user.email, name=db_user.name, region=db_user.region, gender=db_user.gender)
        es.index(index="users", id=db_user.id, body=user_data.dict())

    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        await db.execute(delete(Friend).where(or_(Friend.user_id == user_id, Friend.friend_id == user_id)))
        await db.delete(db_user)
        await db.commit()
        es.delete(index="users", id=db_user.id)

    return db_user
