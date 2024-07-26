from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ..models.introduction_requests import IntroductionRequest
from ..schemas.introduction.introduction_request import IntroductionRequestCreate



class IntroductionRequestService:
    @staticmethod
    async def create_introduction_request(db: AsyncSession, request: IntroductionRequestCreate):
        introduction_request = IntroductionRequest(**request.dict())
        db.add(introduction_request)
        await db.commit()
        await db.refresh(introduction_request)
        return introduction_request

    @staticmethod
    async def get_introduction_requests(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(IntroductionRequest).where(
                and_(
                    IntroductionRequest.intermediary_user_id == user_id,
                    IntroductionRequest.status == "pending"
                )
            )
        )
        return result.scalars().all()

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