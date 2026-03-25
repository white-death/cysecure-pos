from sqlalchemy import Column, String, DateTime
from app.db.base import Base
from datetime import datetime

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    token = Column(String, unique=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
