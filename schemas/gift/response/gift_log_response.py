from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

formatted_timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

class GiftLogResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    friend_id: int
    friend_name: str
    ct_money: int
    updated_at: Optional[datetime] = formatted_timestamp

    class Config:
        from_attributes = True

    @staticmethod
    def from_send_orm(transaction, user_name: str, friend_name: str):
        return GiftLogResponse(
            id=transaction.id,
            user_id=transaction.user_id,
            user_name=user_name,
            friend_id=transaction.friend_id,
            friend_name=friend_name,
            ct_money=transaction.ct_money,
            updated_at=transaction.updated_at
        )

    @staticmethod
    def from_receive_orm(transaction, user_name: str, friend_name: str):
        return GiftLogResponse(
            id=transaction.id,
            user_id=transaction.friend_id,
            user_name=friend_name,
            friend_id=transaction.user_id,
            friend_name=user_name,
            ct_money=transaction.ct_money,
            updated_at=transaction.updated_at
        )

class GiftLogResponseLog(BaseModel):
    transactions: List[GiftLogResponse]

    class Config:
        from_attributes = True
