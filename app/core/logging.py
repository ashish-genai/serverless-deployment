import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logger = logging.getLogger('asset_management')
logger.setLevel(logging.INFO)

# Create handlers
file_handler = RotatingFileHandler(
    'logs/asset_management.log',
    maxBytes=10240000,  # 10MB
    backupCount=5
)
console_handler = logging.StreamHandler()

# Create formatters and add it to handlers
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_activity(user: str, action: str, details: str):
    """Log user activity with details"""
    logger.info(f"User: {user} - Action: {action} - Details: {details}")
    
    # Also store in database
    from ..database import SessionLocal
    from ..models.activity_log import ActivityLog
    
    db = SessionLocal()
    try:
        log = ActivityLog(user=user, action=action, details=details)
        db.add(log)
        db.commit()
    finally:
        db.close()