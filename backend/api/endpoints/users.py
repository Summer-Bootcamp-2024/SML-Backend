from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.crud.auth_crud import get_user_by_email
from Backend.backend.crud.user_crud import create_user, get_user, update_user, delete_user
from Backend.backend.database import get_db
from Backend.backend.schemas.user.user_create import UserCreate
from Backend.backend.schemas.user.user_schema import User
from Backend.backend.schemas.user.user_update import UserUpdate
from Backend.backend.utils.redis_connection import get_redis_connection

router = APIRouter()

# 사용자 회원가입
@router.post("/signup", response_model=User)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db=db, user=user)
    return new_user

# 사용자 프로필 조회
@router.get("/{id}", response_model=User)
async def read_user(id: int, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 사용자 프로필 수정
@router.put("/{id}", response_model=User)
async def update_user_endpoint(id: int, user_update: UserUpdate, session_id: str = Cookie(None), db: AsyncSession = Depends(get_db), redis=Depends(get_redis_connection)):
    # 세션 ID 확인
    if not session_id:
        raise HTTPException(status_code=400, detail="Not logged in")

    # redis에서 세션 ID를 사용해 이메일을 가져오기
    email = await redis.get(session_id)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid session")

    # 이메일을 사용해 데이터베이스에서 사용자 조회
    db_user = await get_user_by_email(db, email=email.decode("utf-8"))
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 사용자 프로필 업데이트
    db_user = await update_user(db, user_id=id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 사용자 프로필 삭제
@router.delete("/{id}", response_model=User)
async def delete_user_endpoint(id: int, db: AsyncSession = Depends(get_db)):
    db_user = await delete_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user