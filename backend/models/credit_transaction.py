from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Backend.backend.database import Base
from Backend.backend.models.user import User

class CreditTransaction(Base):
    __tablename__ = 'credit_transaction'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("friends.id"))
    ct_money = Column(Integer)
    status = Column(String(30))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id], back_populates="transactions")
    friend = relationship("Friend", foreign_keys=[friend_id])


User.transactions = relationship("CreditTransaction", order_by=CreditTransaction.id, back_populates="user")
