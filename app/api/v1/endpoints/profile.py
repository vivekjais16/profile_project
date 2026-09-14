"""
Profile & Competencies API Endpoints
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.portfolio_service import PortfolioService
from app.schemas.profile import ProfileRead, CoreCompetencyRead, MetricStatRead

router = APIRouter(prefix="/profile", tags=["Profile & Overview"])


@router.get("", response_model=ProfileRead, summary="Get Full Profile")
def get_profile(db: Session = Depends(get_db)):
    """Retrieve Vivek Jaiswal's core personal profile, objective, and executive summary."""
    profile = PortfolioService.get_profile(db)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found in database")
    return profile


@router.get("/metrics", response_model=List[MetricStatRead], summary="Get Metric Stats")
def get_metrics(db: Session = Depends(get_db)):
    """Retrieve key career metrics and production stats."""
    return PortfolioService.get_metrics(db)


@router.get("/competencies", response_model=List[CoreCompetencyRead], summary="Get Core Competencies")
def get_competencies(db: Session = Depends(get_db)):
    """Retrieve core technical competencies."""
    return PortfolioService.get_core_competencies(db)
