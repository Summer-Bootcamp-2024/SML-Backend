from sqlalchemy import select, or_, and_

from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.models.friends import Friend

async def request_friend(db: AsyncSession, friend_id: int, user_id: int):
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
    requestFriend = Friend(user_id=user_id, friend_id=friend_id, status='pending')
    responseFriend = Friend(user_id=friend_id, friend_id=user_id, status='pending')
    db.add(requestFriend)
    db.add(responseFriend)
    await db.commit()
    await db.refresh(requestFriend)
    await db.refresh(responseFriend)


async def get_pending_friend(db: AsyncSession, friend_id: int):
    result = await db.execute(
        select(Friend).where(
            and_(Friend.friend_id == friend_id, Friend.status == "pending")
        )
    )
    friend_list = result.scalars().all()
    if not friend_list:
        raise ValueError("존재하지 않는 user_id이거나 status == pending이 존재하지 않음")
    return friend_list

async def accept_friend(db: AsyncSession, friend_id: int, user_id: int, status: str):
    if status not in ["accepted", "rejected"]:
        raise ValueError("유효하지 않은 status 값입니다.")

    result = await db.execute(
        select(Friend).where(
            or_(
                and_(Friend.user_id == user_id, Friend.friend_id == friend_id, Friend.status == "pending"),
                and_(Friend.user_id == friend_id, Friend.friend_id == user_id, Friend.status == "pending")
            )
        )
    )

    friends_to_update = result.scalars().all()

    if not friends_to_update:
        # 결과가 없으면 오류 발생
        raise ValueError("pending인 친구 요청이 없습니다.")
    else:
        # 결과가 있으면 상태 업데이트
        for friend in friends_to_update:
            friend.status = status
        # 데이터베이스에 커밋하여 변경 사항 저장
        await db.commit()
        return f"Status is updated to {status}"