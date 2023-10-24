from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "portfolio"

    user_id = Column(String, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow())
