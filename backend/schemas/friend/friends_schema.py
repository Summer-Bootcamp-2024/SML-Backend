from pydantic import BaseModel

class RequestFriend(BaseModel):
    user_id: int
    friend_id: int
    is_friend: str
    is_deleted: bool = False

