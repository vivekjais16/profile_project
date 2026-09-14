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


@router.get("/resume", summary="Download Vivek Jaiswal Resume (PDF)")
def download_resume(db: Session = Depends(get_db)):
    """Download Vivek Jaiswal's authentic resume PDF."""
    from pathlib import Path
    from fastapi.responses import FileResponse
    from app.core.config import BASE_DIR

    profile = PortfolioService.get_profile(db)
    filename = profile.resume_filename if (profile and profile.resume_filename) else "Vivek_Jaiswal_Resume.pdf"
    file_path = BASE_DIR / "app" / "static" / "resume" / filename

    if not file_path.exists():
        # Fallback to default name if custom filename was provided
        fallback = BASE_DIR / "app" / "static" / "resume" / "Vivek_Jaiswal_Resume.pdf"
        if fallback.exists():
            file_path = fallback
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found")

    return FileResponse(
        path=str(file_path),
        filename="Vivek_Jaiswal_Resume.pdf",
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="Vivek_Jaiswal_Resume.pdf"'},
    )

