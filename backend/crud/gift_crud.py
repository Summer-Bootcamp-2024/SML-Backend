from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from Backend.backend.models.user import User
from Backend.backend.models.credit_transaction import CreditTransaction
from Backend.backend.schemas.gift.request.gift_send import GiftSend

async def create_gift_transaction(db: Session, gift: GiftSend):
    sender_result = await db.execute(select(User).filter(User.id == gift.user_id))
    sender = sender_result.scalars().first()

    receiver_result = await db.execute(select(User).filter(User.id == gift.friend_id))
    receiver = receiver_result.scalars().first()

    connector_result = await db.execute(select(User).filter(User.id == gift.connector_id))
    connector = connector_result.scalars().first()

    if sender and receiver and connector:
        if sender.credit < gift.ct_money:
            return None

        # 크레딧 차감 및 증가
        sender.credit -= gift.ct_money
        receiver.credit += int(gift.ct_money * 0.9)
        connector.credit += int(gift.ct_money * 0.1)

        db.add(sender)
        db.add(receiver)
        db.add(connector)

        # 트랜잭션 기록 생성
        db_gift = CreditTransaction(
            user_id=gift.user_id,
            friend_id=gift.friend_id,
            ct_money=gift.ct_money
        )
        db.add(db_gift)
        await db.commit()
        await db.refresh(db_gift)

        return db_gift

    return None

async def get_user_name(db: AsyncSession, user_id: int) -> str:
    result = await db.execute(select(User.name).filter(User.id == user_id))
    user = result.scalars().first()
    return user if user else "Unknown"