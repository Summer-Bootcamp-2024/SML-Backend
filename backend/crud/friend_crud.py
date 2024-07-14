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

# async def accept_friend(db: AsyncSession, user_id: int):
#     result = await db.execute(
#         select(Friend).where(
#             and_(Friend.friend_id == user_id, Friend.status == "pending")
#         )
#     )

# 1. accept로 바꾸고, user_id == 1 and friend_id == 2 레코드를 하나 더 만든다.
# => 1 2 | 2 1 accept
# 1 친구 목록리스트 1
#
# 2. 1 2 accept
# user_id == 2 and accepted
# friend_id == 2 and accepted