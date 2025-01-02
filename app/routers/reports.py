from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.asset import Asset
from ..models.order import Order, OrderType
from ..dependencies import get_current_user
from ..core.cache import cache
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def report_dashboard(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return templates.TemplateResponse(
        "reports/index.html",
        {"request": request, "current_user": current_user}
    )

@router.get("/asset-value")
@cache(ttl=300)
async def asset_value_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Calculate total asset value by department
    department_values = (
        db.query(
            Asset.department,
            func.sum(Asset.quantity * Asset.unit_price).label('total_value')
        )
        .group_by(Asset.department)
        .all()
    )
    
    return {
        "department_values": [
            {"department": dv[0], "total_value": float(dv[1])}
            for dv in department_values
        ]
    }

@router.get("/department-inventory")
@cache(ttl=300)
async def department_inventory_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get inventory counts by department
    inventory = (
        db.query(
            Asset.department,
            func.count(Asset.id).label('asset_count'),
            func.sum(Asset.quantity).label('total_quantity')
        )
        .group_by(Asset.department)
        .all()
    )
    
    return {
        "inventory": [
            {
                "department": inv[0],
                "asset_count": inv[1],
                "total_quantity": int(inv[2])
            }
            for inv in inventory
        ]
    }

@router.get("/order-history")
@cache(ttl=300)
async def order_history_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get order history summary
    orders = (
        db.query(
            Order.order_type,
            func.count().label('order_count'),
            func.sum(Order.quantity).label('total_quantity')
        )
        .group_by(Order.order_type)
        .all()
    )
    
    return {
        "orders": [
            {
                "type": ot[0],
                "count": ot[1],
                "total_quantity": int(ot[2])
            }
            for ot in orders
        ]
    }