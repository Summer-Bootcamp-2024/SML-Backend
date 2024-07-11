import uuid

from fastapi import Depends, Response, HTTPException, APIRouter, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.backend.crud.auth_crud import get_user_by_email
from Backend.backend.database import get_db
from Backend.backend.schemas.user.user_login import UserLogin
from Backend.backend.utils.redis_connection import get_redis_connection

router = APIRouter()

# 세션 ID 생성 함수
def generate_session_id():
    return str(uuid.uuid4())

@router.post("/login")
async def login_user(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db), redis=Depends(get_redis_connection)):
    db_user = await get_user_by_email(db, email=user.email)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 세션 생성 및 Redis에 저장
    session_id = generate_session_id()
    # await app.state.redis.set(session_id, user.email)
    await redis.set(session_id, user.email)

    # 세션 ID를 쿠키에 저장
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True)

    # 로그인 성공 시 사용자 상태를 "온라인"으로 업데이트
    db_user.status = "온라인"
    await db.commit()  # 데이터베이스에 변경사항을 커밋
    return {"message": "Login successful"}


# 사용자 로그아웃
@router.post("/logout")
async def logout_user(response: Response, session_id: str = Cookie(None), db: AsyncSession = Depends(get_db), redis=Depends(get_redis_connection)):
    if not session_id:  # 쿠키가 없을 경우 예외 처리
        raise HTTPException(status_code=400, detail="Not logged in")

    # 세션 ID를 키로 사용하여 저장된 이메일 가져옮
    # email = await app.state.redis.get(session_id)
    email = await redis.get(session_id)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid session")

    # 데이터베이스에서 사용자 조회
    db_user = await get_user_by_email(db, email=email.decode("utf-8"))
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    # 로그아웃 시 세션 삭제 및 사용자 상태 업데이트
    await redis.delete(session_id)
    response.delete_cookie(key="session_id")

    # 로그아웃 성공 시 사용자 상태를 "오프라인"으로 업데이트
    db_user.status = "오프라인"
    await db.commit()  # 데이터베이스에 변경사항을 커밋
    return {"message": "Logout successful"}