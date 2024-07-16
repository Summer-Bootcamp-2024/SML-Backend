from fastapi import APIRouter

from Backend.backend.api.endpoints import friends, auth, users, relationships, chatrooms, search, messages

api_router = APIRouter(prefix="/api/v1", tags=["api"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(chatrooms.router, prefix="/chatrooms", tags=["chatrooms"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])