from pydantic import BaseModel
from datetime import datetime
from ..models.order import OrderType

class OrderBase(BaseModel):
    order_type: OrderType
    asset_id: int
    quantity: int
    department: str

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True