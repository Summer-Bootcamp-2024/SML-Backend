from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.crud.friend_crud import request_friend, get_pending_friend
from Backend.backend.database import get_db
from Backend.backend.schemas.friend.friends_request import FriendRequest
from Backend.backend.schemas.friend.friends_response import FriendResponse

router = APIRouter()
# 일촌 요청
@router.post("", status_code=status.HTTP_201_CREATED)
async def post_request_friend(request: FriendRequest, db: AsyncSession = Depends(get_db)):
    try:
        await request_friend(db, request.user_id, request.friend_id)
        return {"status": "success", "message": "Friend request sent successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to post_request_friend")

# 일촌 요청 조회
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=List[FriendResponse])
async def get_request_friend(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_friend = await get_pending_friend(db, user_id)
        return db_friend
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, "Failed to get_request_friend.")

# # 일촌 요청 수락/거절
# # @router.put("{id}")
#

