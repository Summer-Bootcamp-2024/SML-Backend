from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.models.credit_transaction import CreditTransaction
from Backend.backend.schemas.gift.response.gift_response import GiftResponse

async def send_transaction(db: AsyncSession, user_id: int):
    result = await db.execute(select(CreditTransaction).filter(CreditTransaction.user_id == user_id))
    transactions = result.scalars().all()
    return [GiftResponse.from_send_orm(tx) for tx in transactions]

async def recieve_transaction(db: AsyncSession, friend_id: int):
    result = await db.execute(select(CreditTransaction).filter(CreditTransaction.friend_id == friend_id))
    transactions = result.scalars().all()
    return [GiftResponse.from_receive_orm(tx) for tx in transactions]
