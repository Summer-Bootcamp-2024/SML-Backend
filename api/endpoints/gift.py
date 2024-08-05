from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_db
from ...crud.gift_crud import create_gift_transaction
from ...schemas.gift.request.gift_send import GiftSend
from ...schemas.gift.response.gift_response import GiftResponse

router = APIRouter()

@router.post("", response_model=GiftResponse)
async def create_gift(gift: GiftSend, db: AsyncSession = Depends(get_db)):
    db_gift = await create_gift_transaction(db, gift)
    if db_gift is None:
        raise HTTPException(status_code=400, detail="Insufficient credits or user not found")
    return db_gift
