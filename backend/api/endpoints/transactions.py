from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.crud.transactions_crud import send_transaction, receive_transaction
from Backend.backend.database import get_db
from Backend.backend.schemas.gift.response.gift_log_response import GiftLogResponseLog

router = APIRouter()

@router.get("/sent/{user_id}", response_model=GiftLogResponseLog)
async def read_gift(user_id: int, db: AsyncSession = Depends(get_db)):
    send_log = await send_transaction(db, user_id=user_id)
    if not send_log:
        raise HTTPException(status_code=404, detail="No sent transactions found for the user")
    return {"transactions": send_log}

@router.get("/received/{user_id}", response_model=GiftLogResponseLog)
async def receive_gift(user_id: int, db: AsyncSession = Depends(get_db)):
    receive_log = await receive_transaction(db, friend_id=user_id)
    if not receive_log:
        raise HTTPException(status_code=404, detail="No received transactions found for the user")
    return {"transactions": receive_log}
