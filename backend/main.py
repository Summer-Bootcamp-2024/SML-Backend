from datetime import datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.models.user import User
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from Backend.backend.api.api import api_router
from Backend.backend.api.endpoints import introduction_request  # 추가
from Backend.backend.database import create_tables, get_db
from Backend.backend.schemas.search.search_schema import UserSearchResult
from Backend.backend.utils.chat import manager
from Backend.backend.utils.index_user import index_users
from Backend.backend.utils.redis_connection import get_redis_connection
from Backend.backend.crud.message_crud import create_message
from Backend.backend.schemas.chat.messages import MessageCreate

origins = [
    "http://localhost:5173"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    await create_tables()
    app.state.redis = get_redis_connection()

    # 유저 데이터를 인덱싱
    async for session in get_db():
        result = await session.execute(select(User))
        users = result.scalars().all()
        user_search_results = [UserSearchResult.from_orm(user) for user in users]
        index_users(user_search_results)
        break  # 한번만 실행하고 break해서 async for 루프 종료해줘야됨

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.aclose()

@app.get("/")
def read_root():
    index_path = Path(__file__).parent / "templates" / "index.html"
    return HTMLResponse(index_path.read_text())

@app.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, client_id: int, session: AsyncSession = Depends(get_db)):
    await manager.connect(websocket, room_id)  # WebSocket 연결 처리
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")

            # 메시지를 데이터베이스에 저장
            message_data = MessageCreate(
                room_id=room_id,
                sender_id=client_id,
                content=data,
                timestamp=datetime.utcnow()
            )
            await create_message(message_data, session)

            # 모든 연결된 클라이언트에게 메시지 브로드캐스트
            message = f"Client #{client_id} in room #{room_id} says: {data}"
            await manager.send_message(room_id, message)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.send_message(room_id, f"Client #{client_id} has left the room {room_id}")
