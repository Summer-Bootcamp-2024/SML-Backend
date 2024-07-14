from pydantic import BaseModel


class FriendAccept(BaseModel):
    user_id: int
    status: str # accepted // rejected