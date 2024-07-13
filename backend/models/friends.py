from sqlalchemy import Column, String, Boolean, ForeignKey, BigInteger, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from Backend.backend.database import Base

class Friend(Base):
    __tablename__ = 'friends'
    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    friend_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    status = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])
