# Backend/backend/api/endpoints/credit.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.database import get_db
from Backend.backend.crud.credit_crud import update_credit
from Backend.backend.schemas.credit.credit_update import CreditUpdate
from Backend.backend.schemas.user.user_schema import User

router = APIRouter()

@router.put("/{user_id}/credit", response_model=User)
async def update_user_credit(user_id: int, credit_update: CreditUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_credit(db, user_id, credit_update.credit)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user