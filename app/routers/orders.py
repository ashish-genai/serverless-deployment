from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..core.logging import log_activity
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.order import Order, OrderType
from ..models.asset import Asset
from ..schemas.order import OrderCreate, OrderResponse
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get("/")
async def list_orders(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order)
    if current_user.role == UserRole.EMPLOYEE:
        orders = orders.filter(Order.created_by == current_user.id)
    orders = orders.all()

    return templates.TemplateResponse(
        "orders/list.html",
        {
            "request": request,
            "current_user": current_user,
            "orders": orders
        }
    )

@router.post("/", response_model=OrderResponse)
@router.get("/create")
async def create_order_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = db.query(Asset).all()
    return templates.TemplateResponse(
        "orders/form.html",
        {
            "request": request,
            "current_user": current_user,
            "assets": assets
        }
    )

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_order = Order(
        **order.dict(),
        created_by=current_user.id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    log_activity(current_user.username, "create_order", f"Created order #{db_order.id}")
    log_activity(current_user.username, "create_order", f"Created order #{db_order.id}")
    return db_order

@router.get("/", response_model=List[OrderResponse])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order)
    if current_user.role == UserRole.EMPLOYEE:
        orders = orders.filter(Order.created_by == current_user.id)
    return orders.offset(skip).limit(limit).all()

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role == UserRole.EMPLOYEE and db_order.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db_order