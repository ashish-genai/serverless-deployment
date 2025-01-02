import json
from typing import Dict, Any
from mangum import Mangum
from fastapi import APIRouter, HTTPException
from ..database import DatabaseManager
from ..models import Order

router = APIRouter()

@router.get("/orders")
async def list_orders(user_id: str = None):
    try:
        orders = await DatabaseManager.list_orders(user_id)
        return {"orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        order = await DatabaseManager.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orders")
async def create_order(order: Dict[str, Any]):
    try:
        # First check if we have enough quantity for outgoing orders
        if order.get('order_type') == 'outgoing':
            asset = await DatabaseManager.get_asset(order['asset_id'])
            if not asset or asset['quantity'] < order['quantity']:
                raise HTTPException(
                    status_code=400, 
                    detail="Insufficient quantity available"
                )
        
        created_order = await DatabaseManager.create_order(order)
        
        # Update asset quantity
        if order.get('order_type') == 'outgoing':
            await DatabaseManager.update_asset(
                order['asset_id'],
                {'quantity': asset['quantity'] - order['quantity']}
            )
        else:
            await DatabaseManager.update_asset(
                order['asset_id'],
                {'quantity': asset['quantity'] + order['quantity']}
            )
            
        return created_order
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))