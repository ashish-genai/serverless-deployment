from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class OrderType(str, enum.Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_type = Column(Enum(OrderType))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    quantity = Column(Integer)
    department = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    asset = relationship("Asset")
    user = relationship("User")