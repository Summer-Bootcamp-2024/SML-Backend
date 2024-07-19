from datetime import datetime
from typing import List
from sqlalchemy.orm import selectinload

from Backend.backend.models.messages import Message
from Backend.backend.models.user import User
from sqlalchemy import delete
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.models.chatrooms import ChatRoom
from Backend.backend.schemas.chat.chatroom_create import ChatroomCreate, ChatroomResponse, ChatroomResponse2


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
        created_at=chatroom.created_at or datetime.utcnow(),
        updated_at=chatroom.updated_at or datetime.utcnow()
    )
    session.add(new_chatroom)
    await session.commit()
    await session.refresh(new_chatroom)
    return new_chatroom

async def get_chatroom(user_id: int, session: AsyncSession) -> List[ChatroomResponse2]:
    query = (
        select(ChatRoom)
        .options(
            selectinload(ChatRoom.user1),
            selectinload(ChatRoom.user2),
        )
        .where((ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id))
    )
    result = await session.execute(query)
    chatrooms = result.scalars().all()


    response = []
    for chatroom in chatrooms:
        user1 = chatroom.user1
        user2 = chatroom.user2

        response.append(ChatroomResponse2(
            id=chatroom.id,
            user1_id=user1.id,
            user1_name=user1.name,
            user1_image_url=user1.image_url,
            user2_id=user2.id,
            user2_name=user2.name,
            user2_image_url=user2.image_url,
            created_at=chatroom.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=chatroom.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        ))

    return response

async def delete_chatroom(room_id: int, session: AsyncSession):
    # 주어진 room_id에 해당하는 메시지 삭제
    await session.execute(
        delete(Message).where(Message.room_id == room_id)
    )
    await session.commit()

    # 주어진 room_id에 해당하는 채팅방 삭제
    result = await session.execute(
        select(ChatRoom).where(ChatRoom.id == room_id)
    )
    chatroom = result.scalars().first()
    if chatroom:
        await session.delete(chatroom)
        await session.commit()
    else:
        raise HTTPException(status_code=404, detail="Chatroom not found")

    return Response(status_code=204)
