from pydantic import BaseModel
from datetime import datetime

class GiftResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    ct_money: int
    updated_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def from_send_orm(transaction):
        return GiftResponse(
            id=transaction.id,
            user_id=transaction.user_id,
            friend_id=transaction.friend_id,
            ct_money=transaction.ct_money,
            updated_at=transaction.updated_at
        )

    @staticmethod
    def from_receive_orm(transaction):
        return GiftResponse(
            id=transaction.id,
            user_id=transaction.friend_id,  # recieve에선 해당 위치 바꿈 why? 같은 스키마로 활용하기 때문, 프론트지장 x
            friend_id=transaction.user_id,
            ct_money=transaction.ct_money,
            updated_at=transaction.updated_at
        )