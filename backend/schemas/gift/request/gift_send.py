from pydantic import BaseModel

class GiftSend(BaseModel):
    user_id: int
    connector_id: int  # 주선자의 id를 받기 위해 추가
    friend_id: int
    ct_money: int
