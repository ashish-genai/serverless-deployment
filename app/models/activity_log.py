from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
from datetime import datetime

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    action = Column(String)
    details = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)