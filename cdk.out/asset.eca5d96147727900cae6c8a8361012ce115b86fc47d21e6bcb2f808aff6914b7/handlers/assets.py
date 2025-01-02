import json
from typing import Dict, Any
from mangum import Mangum
from fastapi import APIRouter, HTTPException
from ..database import DatabaseManager
from ..models import Asset

router = APIRouter()

@router.get("/assets")
async def list_assets():
    try:
        assets = await DatabaseManager.list_assets()
        return {"assets": assets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/{asset_id}")
async def get_asset(asset_id: str):
    try:
        asset = await DatabaseManager.get_asset(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assets")
async def create_asset(asset: Dict[str, Any]):
    try:
        created_asset = await DatabaseManager.create_asset(asset)
        return created_asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/assets/{asset_id}")
async def update_asset(asset_id: str, asset: Dict[str, Any]):
    try:
        updated_asset = await DatabaseManager.update_asset(asset_id, asset)
        if not updated_asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return updated_asset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/assets/{asset_id}")
async def delete_asset(asset_id: str):
    try:
        # First check if asset exists
        asset = await DatabaseManager.get_asset(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # Delete the asset
        await DatabaseManager.delete_asset(asset_id)
        return {"status": "success", "message": "Asset deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))