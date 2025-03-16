from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Fulfillment(Base):
    __tablename__ = "fulfillments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    is_fulfilled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    fulfilled_at = Column(DateTime, nullable=True) 