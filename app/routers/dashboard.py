from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.asset import Asset
from ..models.order import Order
from ..dependencies import get_current_user
from ..core.cache import cache, CacheManager
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
@cache(ttl=60)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get asset statistics
    asset_stats = db.query(
        func.count(Asset.id).label("count"),
        func.sum(Asset.quantity * Asset.unit_price).label("total_value")
    ).first()

    # Get order statistics
    recent_order_count = db.query(func.count(Order.id))\
        .filter(Order.created_at >= func.date('now', '-7 days'))\
        .scalar()

    # Get recent activities (placeholder - implement actual activity logging)
    recent_activities = []

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "asset_count": asset_stats.count,
            "total_value": asset_stats.total_value or 0,
            "recent_order_count": recent_order_count,
            "pending_order_count": 0,  # Implement pending order logic
            "recent_activities": recent_activities
        }
    )