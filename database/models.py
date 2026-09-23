from sqlalchemy import Column, String, BIGINT, Boolean
from database.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key = True)
    username = Column(String(225))
    email = Column(String(225))
    password_hash = Column(String(255))
    is_active = Column(Boolean, default = True)
    