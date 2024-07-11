from fastapi import APIRouter

from Backend.backend.api.endpoints import friends, auth, users

api_router = APIRouter(prefix="/api/v1", tags=["api"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(friends.router, prefix="/friends", tags=["friends"])