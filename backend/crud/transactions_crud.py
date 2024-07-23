from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.models.credit_transaction import CreditTransaction
from Backend.backend.schemas.gift.response.gift_log_response import GiftLogResponse
from Backend.backend.crud.gift_crud import get_user_name

async def send_transaction(db: AsyncSession, user_id: int):
    # 트랜잭션을 조회합니다.
    result = await db.execute(select(CreditTransaction).filter(CreditTransaction.user_id == user_id))
    transactions = result.scalars().all()

    # 사용자 이름과 친구 이름을 조회합니다.
    user_names = {user_id: await get_user_name(db, user_id)}
    friend_ids = {tx.friend_id for tx in transactions}
    for friend_id in friend_ids:
        user_names[friend_id] = await get_user_name(db, friend_id)

    # 응답에 사용자 이름을 추가합니다.
    return [
        GiftLogResponse.from_send_orm(tx, user_names.get(tx.user_id, "Unknown"), user_names.get(tx.friend_id, "Unknown"))
        for tx in transactions
    ]

async def receive_transaction(db: AsyncSession, friend_id: int):
    # 트랜잭션을 조회합니다.
    result = await db.execute(select(CreditTransaction).filter(CreditTransaction.friend_id == friend_id))
    transactions = result.scalars().all()

    # 사용자 이름과 친구 이름을 조회합니다.
    user_ids = {tx.user_id for tx in transactions}
    user_names = {friend_id: await get_user_name(db, friend_id)}
    for user_id in user_ids:
        user_names[user_id] = await get_user_name(db, user_id)

    # 응답에 사용자 이름을 추가합니다.
    return [
        GiftLogResponse.from_receive_orm(tx, user_names.get(tx.user_id, "Unknown"), user_names.get(tx.friend_id, "Unknown"))
        for tx in transactions
    ]
