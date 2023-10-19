from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    userid = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    pass_store_type = Column(String, default="plaintext")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow())
