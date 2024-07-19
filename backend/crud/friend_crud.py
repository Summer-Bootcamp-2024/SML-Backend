from sqlalchemy import select, or_, and_

from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.models.chatrooms import ChatRoom
from Backend.backend.models.friends import Friend
from Backend.backend.models.messages import Message


# 일촌 요청
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

# 일촌 요청 조회
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

# 알촌 수락/거절
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
    elif status == "rejected":
        # 거절인 경우 불필요한 데이터이므로 삭제
        for friend in friends_to_update:
            await db.delete(friend)
    else:
        # 수락인 경우
        for friend in friends_to_update:
            friend.status = status
    # 데이터베이스에 커밋하여 변경 사항 저장
    await db.commit()
    return f"Status is updated to {status}"

# 일촌 리스트 조회
async def list_friend(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Friend).where(
            and_(Friend.user_id == user_id, Friend.status == "accepted")
        )
    )
    friend_list = result.scalars().all()
    if not friend_list:
        raise ValueError("존재하지 않는 user_id이거나 친구가 존재하지 않음.")
    return friend_list

# 일촌 삭제
async def remove_friend(db: AsyncSession, friend_id: int, user_id: int):
    # 1. 친구 관계 가져오기
    result = await db.execute(
        select(Friend).where(
            or_(
                and_(Friend.friend_id == friend_id, Friend.user_id == user_id, Friend.status == "accepted"),
                and_(Friend.friend_id == user_id, Friend.user_id == friend_id, Friend.status == "accepted")
            )
        )
    )
    deleted_friend = result.scalars().all()

    if not deleted_friend:
        raise ValueError("존재하지 않는 user_id이거나 friend_id이다. 혹은 친구가 존재하지 않음.")

    # 2. 채팅방 가져오기
    chatroom_result = await db.execute(
        select(ChatRoom).where(
            or_(
                and_(ChatRoom.user1_id == user_id, ChatRoom.user2_id == friend_id),
                and_(ChatRoom.user1_id == friend_id, ChatRoom.user2_id == user_id)
            )
        )
    )
    chatrooms = chatroom_result.scalars().all()

    # 3. 메시지 삭제
    for chatroom in chatrooms:
        messages_result = await db.execute(
            select(Message).where(Message.room_id == chatroom.id)
        )
        messages = messages_result.scalars().all()
        for message in messages:
            await db.delete(message)
        await db.commit()  # 메시지 삭제 후 커밋

    # 4. 채팅방 삭제
    for chatroom in chatrooms:
        await db.delete(chatroom)
    await db.commit()  # 채팅방 삭제 후 커밋

    # 5. 친구 관계 삭제
    for friend in deleted_friend:
        await db.delete(friend)
    await db.commit()  # 친구 관계 삭제 후 커밋
