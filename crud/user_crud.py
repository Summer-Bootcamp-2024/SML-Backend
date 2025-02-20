from fastapi import UploadFile, File
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.chatrooms import ChatRoom
from ..models.friends import Friend
from ..models.messages import Message
from ..models.user import User
from ..schemas.search.search_schema import UserSearchResult
from ..schemas.user.user_create import UserCreate
from ..schemas.user.user_update import UserUpdate
from ..utils.index_user import es
from ..utils.s3_util import create_s3_url


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        email=user.email,
        password=user.password,
        name=user.name,
        age=user.age,
        gender=user.gender,
        job=user.job,
        category=user.category
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    user_data = UserSearchResult.from_orm(db_user)
    es.index(index="users", id=db_user.id, body=user_data.dict())

    return db_user

# 사용자 업데이트
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)

        user_data = UserSearchResult.from_orm(db_user)
        es.index(index="users", id=db_user.id, body=user_data.dict())

    return db_user

# 사용자 프로필 이미지 업데이트
async def update_profile_img(db: AsyncSession, user_id: int, file: UploadFile = File(...)):
    db_user = await get_user(db, user_id)
    db_user.image_url = await create_s3_url(file)

    await db.commit()
    await db.refresh(db_user)

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



