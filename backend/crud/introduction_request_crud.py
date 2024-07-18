from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from Backend.backend.models.introduction_requests import IntroductionRequest
from Backend.backend.schemas.introduction.introduction_request import IntroductionRequestCreate, IntroductionRequestUpdate

class IntroductionRequestService:
    @staticmethod
    async def create_introduction_request(db: AsyncSession, request: IntroductionRequestCreate):
        introduction_request = IntroductionRequest(**request.dict())
        db.add(introduction_request)
        await db.commit()
        await db.refresh(introduction_request)
        return introduction_request

    @staticmethod
    async def update_introduction_request(db: AsyncSession, request_id: int, status: str):
        result = await db.execute(
            select(IntroductionRequest).where(IntroductionRequest.id == request_id)
        )
        introduction_request = result.scalars().first()
        if introduction_request is None:
            raise ValueError("Introduction request not found")

        introduction_request.status = status
        await db.commit()
        await db.refresh(introduction_request)
        return introduction_request
