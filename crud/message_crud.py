from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.messages import Message
from ..schemas.chat.messages import MessageCreate

async def create_message(message: MessageCreate, session: AsyncSession) -> Message:
    new_message = Message(
        room_id=message.room_id,
        sender_id=message.sender_id,
        content=message.content,
        timestamp=message.timestamp
    )
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)
    return new_message

async def get_messages(chatroom_id: int, session: AsyncSession) -> List[Message]:
    query = select(Message).filter(Message.room_id == chatroom_id)
    result = await session.execute(query)
    messages = result.scalars().all()
    return messages
