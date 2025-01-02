from pydantic import BaseModel
from datetime import datetime

class ActivityLog(BaseModel):
    id: int
    user: str
    action: str
    details: str
    created_at: datetime

    class Config:
        orm_mode = True