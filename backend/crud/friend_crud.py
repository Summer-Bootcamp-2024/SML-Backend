from sqlalchemy import select, or_, and_

from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.models.friends import Friend

async def request_friend(db: AsyncSession, user_id: int, friend_id: int):
    # user_id와 friend_id가 같은 값인지
    if user_id == friend_id:
        raise ValueError("user_id와 friend_id 값이 같음")

    # 이미 DB에 존재하는지 검사
    existing_friendship = await db.execute(
        select(Friend).where(
            or_(
                and_(Friend.user_id == user_id, Friend.friend_id == friend_id),
                and_(Friend.user_id == friend_id, Friend.friend_id == user_id)
            )
        )
    )
    if existing_friendship.scalars().first():
        raise ValueError("이미 DB에 존재하는 값입니다.")

    # Friend 모델 인스턴스 생성
    new_friend = Friend(user_id=user_id, friend_id=friend_id, status='pending')
    db.add(new_friend)
    await db.commit()
    await db.refresh(new_friend)
