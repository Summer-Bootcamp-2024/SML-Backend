from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_db
from ...crud.message_crud import get_messages
from ...schemas.chat.messages import MessageResponse

router = APIRouter()


@router.get("/{room_id}", response_model=List[MessageResponse])
async def get_room_messages(room_id: int, session: AsyncSession = Depends(get_db)):
    messages = await get_messages(room_id, session)
    return messages
