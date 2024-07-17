from datetime import datetime
from typing import List
from sqlalchemy.orm import joinedload
from Backend.backend.models.user import User
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.models.chatrooms import ChatRoom
from Backend.backend.schemas.chat.chatroom_create import ChatroomCreate, ChatroomResponse


async def create_chatroom(chatroom: ChatroomCreate, session: AsyncSession) -> ChatRoom:
    # 기존 채팅방 유무 확인
    existing_chatroom_query = select(ChatRoom).where(
        ((ChatRoom.user1_id == chatroom.user1_id) & (ChatRoom.user2_id == chatroom.user2_id)) |
        ((ChatRoom.user1_id == chatroom.user2_id) & (ChatRoom.user2_id == chatroom.user1_id))
    )
    result = await session.execute(existing_chatroom_query)
    existing_chatroom = result.scalars().first()

    if existing_chatroom:
        raise HTTPException(status_code=400, detail="Chatroom between these users already exists")

    new_chatroom = ChatRoom(
        user1_id=chatroom.user1_id,
        user2_id=chatroom.user2_id,
        created_at=chatroom.created_at or datetime.datetime.utcnow(),
        updated_at=chatroom.updated_at or datetime.datetime.utcnow()
    )
    session.add(new_chatroom)
    await session.commit()
    await session.refresh(new_chatroom)
    return new_chatroom


async def get_chatroom(user_id: int, session: AsyncSession) -> List[ChatRoom]:
    query = select(ChatRoom).options(
        joinedload(ChatRoom.user1).load_only(User.id, User.image_url),
        joinedload(ChatRoom.user2).load_only(User.id, User.image_url)
    ).where((ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id))

    result = await session.execute(query)
    chatrooms = result.scalars().all()

    return [
        ChatroomResponse(
            id=chatroom.id,
            user1_id=chatroom.user1_id,
            user1_name=chatroom.user1.name,
            user1_image_url=chatroom.user1.image_url,
            user2_id=chatroom.user2_id,
            user2_name=chatroom.user2.name,
            user2_image_url=chatroom.user2.image_url,
            created_at=chatroom.created_at,
            updated_at=chatroom.updated_at
        ) for chatroom in chatrooms
    ]