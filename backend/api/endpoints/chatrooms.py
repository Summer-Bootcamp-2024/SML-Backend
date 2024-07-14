from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.database import get_db
from Backend.backend.models.chatrooms import ChatRoom
from Backend.backend.crud.chatroom_crud import create_chatroom, get_chatroom
from Backend.backend.schemas.chat.chatroom_create import ChatroomCreate

router = APIRouter()

@router.post("/", response_model=ChatroomCreate)
async def create_chatrooms(chatroom: ChatroomCreate, session: AsyncSession = Depends(get_db)):
    return await create_chatroom(chatroom, session)

@router.get("/{user_id}", response_model=List[ChatroomCreate])
async def get_chatrooms(user_id: int, session: AsyncSession = Depends(get_db)):
    show_chatroom = await get_chatroom(user_id, session)
    if not show_chatroom:
        raise HTTPException(status_code=404, detail="No chatrooms found")
    return show_chatroom



# @router.delete("/{user_id}")
