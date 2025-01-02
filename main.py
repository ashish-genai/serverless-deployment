import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.routers import assets, users, orders, auth, dashboard
from fastapi.middleware.cors import CORSMiddleware
from app.core import security

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Asset Management System",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure HTTPS
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(assets.router)
app.include_router(orders.router)
app.include_router(reports.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)