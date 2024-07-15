from typing import List, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.models.friends import Friend
from Backend.backend.schemas.friend.response.friends_related import FriendsFind

async def get_friends(user_id: int, session: AsyncSession, depth: int = 1, max_depth: int = 3, visited: Set[int] = None, initial_user_id: int = None) -> List[FriendsFind]:
    if visited is None:
        visited = set()

    if initial_user_id is None:
        initial_user_id = user_id  # 초기 호출 시 초기화

    query = (
        select(Friend)
        .where(
            Friend.status == "accepted",
            Friend.user_id == user_id,
            Friend.is_deleted == False
        )
    )
    result = await session.execute(query)
    friends = result.scalars().all()

    friend_list = []
    for friend in friends:
        friend_id = friend.friend_id
        friends_find = FriendsFind(user_id=user_id, friend_id=friend_id, is_deleted=friend.is_deleted)
        if friend_id != initial_user_id:
            friend_list.append(friends_find)
        if depth < max_depth and friend_id not in visited:
            sub_friends = await get_friends(friend_id, session, depth + 1, max_depth, visited, initial_user_id=initial_user_id)  # initial_user_id 전달
            # Only add friends of friends if depth is less than max_depth - 1
            if depth + 1 < max_depth:
                friend_list.extend(sub_friends)

    return friend_list