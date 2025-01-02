from typing import Any, Dict, Optional
from pydantic import BaseModel, validator
import re
from decimal import Decimal

class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(self.message)

def validate_password(password: str) -> None:
    """Validate password strength"""
    if len(password) < 8:
        raise ValidationError("password", "Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("password", "Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValidationError("password", "Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValidationError("password", "Password must contain at least one number")

def validate_email(email: str) -> None:
    """Validate email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError("email", "Invalid email format")

def validate_asset_data(data: Dict[str, Any]) -> None:
    """Validate asset data"""
    if not data.get("name"):
        raise ValidationError("name", "Asset name is required")
    if not data.get("type_id"):
        raise ValidationError("type_id", "Asset type is required")
    if not data.get("department"):
        raise ValidationError("department", "Department is required")
    
    quantity = data.get("quantity")
    if not quantity or int(quantity) < 0:
        raise ValidationError("quantity", "Quantity must be a positive number")
    
    unit_price = data.get("unit_price")
    if not unit_price or Decimal(str(unit_price)) < 0:
        raise ValidationError("unit_price", "Unit price must be a positive number")