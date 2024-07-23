from pydantic import BaseModel

class GiftSend(BaseModel):
    user_id: int
    friend_id: int
    ct_money: int
