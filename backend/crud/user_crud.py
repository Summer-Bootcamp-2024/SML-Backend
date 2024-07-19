from sqlalchemy import delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Backend.backend.models.chatrooms import ChatRoom
from Backend.backend.models.friends import Friend
from Backend.backend.models.messages import Message
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
        password=user.password,
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


# 사용자 삭제
async def delete_user(session: AsyncSession, user_id: int) -> User:
    # 해당 사용자가 포함된 모든 메시지 삭제
    # 사용자가 속한 채팅방 리스트를 가져옴
    result = await session.execute(
        select(ChatRoom.id).where((ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id))
    )
    chatroom_ids = [row[0] for row in result]

    # 각 채팅방에 속한 메시지를 삭제
    for room_id in chatroom_ids:
        await session.execute(
            delete(Message).where(Message.room_id == room_id)
        )

    await session.commit()

    # 해당 사용자가 포함된 모든 채팅방 삭제
    await session.execute(
        delete(ChatRoom).where((ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id))
    )
    await session.commit()

    # 해당 사용자가 포함된 모든 친구 관계 삭제
    await session.execute(
        delete(Friend).where((Friend.user_id == user_id) | (Friend.friend_id == user_id))
    )
    await session.commit()

    # 그 후 사용자 삭제
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        await session.delete(user)
        await session.commit()
    return user
