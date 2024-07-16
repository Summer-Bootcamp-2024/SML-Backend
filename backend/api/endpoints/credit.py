from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.database import get_db
from Backend.backend.crud.credit_crud import update_credit
from Backend.backend.schemas.credit.credit_update import CreditUpdate, CreditResponse

router = APIRouter()

@router.put("/{id}/credit", response_model=CreditResponse)
async def update_user_credit(id: int, credit_update: CreditUpdate, db: AsyncSession = Depends(get_db)):
    user = await update_credit(db, id, credit_update.credits)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return CreditResponse(id=user.id, credit=user.credit, updated_at=user.updated_at)
