from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_db
from ...crud.chatroom_crud import create_chatroom, get_chatroom, delete_chatroom
from ...schemas.chat.chatroom_create import ChatroomCreate, ChatroomResponse, ChatroomResponse2, DeleteResponse


router = APIRouter()

@router.post("/", response_model=ChatroomResponse)
async def create_chatrooms(chatroom: ChatroomCreate, session: AsyncSession = Depends(get_db)):
    return await create_chatroom(chatroom, session)

@router.get("/{user_id}", response_model=List[ChatroomResponse2])
async def get_chatrooms(user_id: int, session: AsyncSession = Depends(get_db)):
    show_chatroom = await get_chatroom(user_id, session)
    if not show_chatroom:
        raise HTTPException(status_code=404, detail="No chatrooms found")
    return show_chatroom

@router.delete("/{room_id}", response_model=DeleteResponse)
async def delete_chatrooms(room_id: int, session: AsyncSession = Depends(get_db)):
    return await delete_chatroom(room_id, session)
