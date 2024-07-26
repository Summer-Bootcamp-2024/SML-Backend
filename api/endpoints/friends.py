from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_db
from ...crud.friend_crud import request_friend, get_pending_friend, accept_friend, list_friend, remove_friend
from ...schemas.friend.request.friends_request import FriendRequest
from ...schemas.friend.response.friends_pending import FriendPending
from ...schemas.friend.request.friends_accept import FriendAccept

router = APIRouter()
# 일촌 요청
@router.post("/{friend_id}", status_code=status.HTTP_201_CREATED)
async def post_request_friend(friend_id: int, request: FriendRequest, db: AsyncSession = Depends(get_db)):
    try:
        await request_friend(db, friend_id, request.user_id)
        return {"status": "success", "message": "Friend request sent successfully."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to post_request_friend")

# 일촌 요청 조회
@router.get("/{friend_id}", status_code=status.HTTP_200_OK, response_model=List[FriendPending])
async def get_request_friend(friend_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_friend = await get_pending_friend(db, friend_id)
        return db_friend
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, "Failed to get_request_friend.")

# 일촌 요청 수락/거절
@router.put("/{friend_id}", status_code=status.HTTP_200_OK)
async def put_request_friend(friend_id: int, request: FriendAccept, db: AsyncSession = Depends(get_db)):
    try:
        message = await accept_friend(db, friend_id, request.user_id, request.status)
        return {"status": "success", "message": message}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, "Failed to put_request_friend.")

# 일촌 리스트 조회
@router.get("/list/{user_id}", status_code=status.HTTP_200_OK, response_model=List[FriendPending])
async def get_friend_list(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        db_friend = await list_friend(db, user_id)
        return db_friend
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, "Failed to get_friend_list.")

# 일촌 삭제
@router.delete("/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_friend(friend_id: int, request: FriendRequest, db: AsyncSession = Depends(get_db)):
    try:
        await remove_friend(db, friend_id, request.user_id)
        return
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(500, "Failed to put_request_friend.")
