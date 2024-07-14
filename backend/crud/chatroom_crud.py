from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.models.chatrooms import ChatRoom
from Backend.backend.schemas.chat.chatroom_create import ChatroomCreate

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
    query = select(ChatRoom).where((ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id))
    result = await session.execute(query)
    return result.scalars().all()