from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.crud.friend_crud import request_friend
from Backend.backend.database import get_db
from Backend.backend.schemas.friend.friends_request import FriendRequest

router = APIRouter()
# 일촌 요청
@router.post("", status_code=status.HTTP_201_CREATED)
async def post_request_friend(request: FriendRequest, db: AsyncSession = Depends(get_db)):
    try:
        await request_friend(db, request.user_id, request.friend_id)
        return {"code": "success", "message": "Friend request sent successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process friend request")

# # 일촌 요청 수락/거절
# # @router.put("{id}")
#
# # 일촌 요청 조회
# # @router.get("{id}")
