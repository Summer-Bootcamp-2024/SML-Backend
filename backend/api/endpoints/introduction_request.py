from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.crud.introduction_request_crud import IntroductionRequestService
from Backend.backend.database import get_db
from Backend.backend.schemas.introduction.introduction_request import IntroductionRequestCreate, IntroductionRequest, IntroductionRequestUpdate

router = APIRouter()

# 소개 요청 생성
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IntroductionRequest)
async def create_introduction_request(request: IntroductionRequestCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await IntroductionRequestService.create_introduction_request(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 소개 요청 수락/거절
@router.put("/{request_id}", status_code=status.HTTP_200_OK, response_model=IntroductionRequest)
async def update_introduction_request(request_id: int, status: IntroductionRequestUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await IntroductionRequestService.update_introduction_request(db, request_id, status.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
