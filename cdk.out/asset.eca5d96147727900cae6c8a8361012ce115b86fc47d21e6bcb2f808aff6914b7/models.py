from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    email: str
    role: str = 'employee'
    created_at: Optional[str] = None

class Asset(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type_id: str
    department: str
    quantity: int
    unit_price: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class Order(BaseModel):
    id: str
    order_type: str
    asset_id: str
    quantity: int
    department: str
    created_by: str
    created_at: Optional[str] = None