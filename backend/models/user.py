from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger
from sqlalchemy.sql import func

from Backend.backend.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    name = Column(String(255))
    age = Column(Integer)
    job = Column(String(255))
    gender = Column(String(255))
    company = Column(String, nullable=True)
    region = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    image_url = Column(String, nullable=True)
    status = Column(String(255), default='오프라인')
    credit = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())