# from fastapi import APIRouter
#
# from Backend.backend.models.friends import Friend
# from Backend.backend.schemas import friends_schema
# from Backend.backend.database import async_session
#
# router = APIRouter()
#
# # 일촌 요청
# @router.post("")
# async def request_friend(friend: friends_schema.RequestFriend):
#     async with async_session() as session:
#         new_friend = Friend(**friend.dict())
#         session.add(new_friend)
#         await session.commit()
#         await session.refresh(new_friend)
#         return new_friend
#
# # @router.get("/users/{user_id}")
# # async def read_user(user_id: int):
# #     async with async_session() as session:
# #         user = await session.get(User, user_id)
# #         if not user:
# #             raise HTTPException(status_code=404, detail="User not found")
# #         return user
#
# # 일촌 요청 수락/거절
# # @router.put("{id}")
#
# # 일촌 요청 조회
# # @router.get("{id}")
