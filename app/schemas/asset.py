from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssetTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class AssetTypeCreate(AssetTypeBase):
    pass

class AssetBase(BaseModel):
    name: str
    description: Optional[str] = None
    type_id: int
    department: str
    quantity: int
    unit_price: float

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type_id: Optional[int] = None
    department: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class AssetResponse(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True