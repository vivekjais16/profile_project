"""
Work Experience API Endpoints
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.portfolio_service import PortfolioService
from app.schemas.experience import WorkExperienceRead

router = APIRouter(prefix="/experiences", tags=["Experience"])


@router.get("", response_model=List[WorkExperienceRead], summary="Get Career Work Experiences")
def get_experiences(db: Session = Depends(get_db)):
    """Retrieve full professional timeline with role highlights, architectural achievements, and tech stacks."""
    return PortfolioService.get_experiences(db)
