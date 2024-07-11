# from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean
# from sqlalchemy.sql import func
#
# from Backend.backend.database import Base
#
# class Friend(Base):
#     __tablename__ = 'friend'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     friend_id = Column(Integer, ForeignKey('user.id'))
#     is_friend = Column(String)
#     is_deleted = Column(Boolean)
#     created_at = Column(TIMESTAMP, server_default=func.now())
#     updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
