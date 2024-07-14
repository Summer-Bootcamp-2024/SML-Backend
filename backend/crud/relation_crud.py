from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.models.friends import Friend
from Backend.backend.schemas.friend.response.friends_related import FriendsFind


async def get_friends(user_id: int, session: AsyncSession, depth: int = 1, max_depth: int = 3, visited: set = None) -> List[FriendsFind]:
    query = (
        select(Friend)
        .where(
            user_id == Friend.user_id
        )
    )
    result = await session.execute(query)
    friends = result.scalars().all()

    friend_list = []
    for friend in friends:
        friend_id = friend.friend_id
        friends_find = FriendsFind(user_id=user_id, friend_id=friend_id, is_deleted=friend.is_deleted)
        friend_list.append(friends_find)
        if depth < max_depth:
            sub_friends = await get_friends(friend_id, session, depth + 1, max_depth, visited)
            friend_list.extend(sub_friends)

    return friend_list


