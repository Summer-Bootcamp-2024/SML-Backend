from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from Backend.backend.schemas.introduction.introduction_request import IntroductionRequest, IntroductionRequestCreate, IntroductionRequestUpdate
from Backend.backend.crud.introduction_request_crud import IntroductionRequestService
from Backend.backend.database import get_db

router = APIRouter()

@router.post("/introduction_requests/", response_model=IntroductionRequest)
async def create_request(request: IntroductionRequestCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await IntroductionRequestService.create_introduction_request(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/introduction_requests/", response_model=List[IntroductionRequest])
async def read_requests(user_id: int, db: AsyncSession = Depends(get_db)):
    return await IntroductionRequestService.get_introduction_requests(db, user_id)

@router.put("/introduction_requests/{request_id}", response_model=IntroductionRequest)
async def update_request(request_id: int, status: IntroductionRequestUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await IntroductionRequestService.update_introduction_request(db, request_id, status.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
