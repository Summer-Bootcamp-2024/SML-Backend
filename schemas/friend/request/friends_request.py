from pydantic import BaseModel


class FriendRequest(BaseModel):
    user_id: int