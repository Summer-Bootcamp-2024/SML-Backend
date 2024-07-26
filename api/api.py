from fastapi import APIRouter

from .endpoints import relationships, search
from .endpoints import introduction_request, auth, friends, users, credit, messages, chatrooms, transactions, gift


api_router = APIRouter(prefix="/api/v1", tags=["api"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(friends.router, prefix="/friends", tags=["friends"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(chatrooms.router, prefix="/chatrooms", tags=["chatrooms"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(credit.router, prefix="/users", tags=["credit"])
api_router.include_router(gift.router, prefix="/gifts", tags=["gift"])
api_router.include_router(introduction_request.router, prefix="/introduction_request", tags=["introduction_request"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])



