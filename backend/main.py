from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from Backend.backend.api.api import api_router
from Backend.backend.database import create_tables
from Backend.backend.utils.redis_connection import get_redis_connection

origins = [
    "*"
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

# main.py에서는 이렇게 사용

@app.on_event("startup")
async def startup_event():
    await create_tables()
    app.state.redis = get_redis_connection()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

