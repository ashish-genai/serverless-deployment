from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..core.logging import log_activity
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.asset import Asset, AssetType
from ..schemas.asset import AssetCreate, AssetUpdate, AssetResponse, AssetTypeCreate
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/assets",
    tags=["assets"]
)

@router.post("/types", response_model=AssetTypeCreate)
async def create_asset_type(
    asset_type: AssetTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_asset_type = AssetType(**asset_type.dict())
    db.add(db_asset_type)
    db.commit()
    db.refresh(db_asset_type)
    return db_asset_type

@router.get("/create")
async def create_asset_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    asset_types = db.query(AssetType).all()
    return templates.TemplateResponse(
        "assets/form.html",
        {
            "request": request,
            "current_user": current_user,
            "asset_types": asset_types,
            "asset": None
        }
    )

@router.get("/")
async def list_assets(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = db.query(Asset).all()
    return templates.TemplateResponse(
        "assets/list.html",
        {
            "request": request,
            "current_user": current_user,
            "assets": assets
        }
    )

@router.post("/", response_model=AssetResponse)
async def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/", response_model=List[AssetResponse])
@cache(ttl=300)  # Cache for 5 minutes
async def read_assets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assets = db.query(Asset).offset(skip).limit(limit).all()
    return assets

@router.get("/{asset_id}/edit")
async def edit_asset_form(
    asset_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    asset_types = db.query(AssetType).all()
    return templates.TemplateResponse(
        "assets/form.html",
        {
            "request": request,
            "current_user": current_user,
            "asset": asset,
            "asset_types": asset_types
        }
    )

@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    log_activity(current_user.username, "delete_asset", f"Deleted asset {db_asset.name}")
    db.delete(db_asset)
    db.commit()
    return {"success": True}

@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    for key, value in asset.dict(exclude_unset=True).items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset