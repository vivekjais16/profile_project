"""
Health & System Diagnostic API Endpoints
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import Dict, Any
import os
import platform
import time
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db

router = APIRouter(tags=["System Health & Diagnostics"])

START_TIME = time.time()


@router.get("/health", status_code=status.HTTP_200_OK, summary="Service Health Check")
def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Verify backend responsiveness and SQLite database connectivity."""
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "database": db_status,
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


@router.get("/system-status", status_code=status.HTTP_200_OK, summary="Detailed System Status")
def system_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retrieve detailed backend runtime diagnostics, OS information, and database engine."""
    return {
        "project": settings.PROJECT_NAME,
        "developer": settings.AUTHOR_NAME,
        "email": settings.AUTHOR_EMAIL,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "environment": settings.ENVIRONMENT,
        "database_engine": "SQLite 3 (WAL Mode enabled)",
        "sqlite_db_exists": os.path.exists(settings.DATA_DIR / "portfolio.db"),
    }
