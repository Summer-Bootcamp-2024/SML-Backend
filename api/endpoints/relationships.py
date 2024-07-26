from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ...crud.relation_crud import get_friends
from ...database import get_db
from ...schemas.friend.response.friends_related import FriendsFind

router = APIRouter()


@router.get("/{id}", response_model=List[FriendsFind])
async def get_relationships(id: int, session: AsyncSession = Depends(get_db)):
    friend_relationships = await get_friends(id, session)
    if not friend_relationships:
        raise HTTPException(status_code=404, detail="No friend relationships found")
    for friend in friend_relationships:  # 각 관계를 출력
        print(friend)
    return friend_relationships



