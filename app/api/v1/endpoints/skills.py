"""
Skills & Technical Stack API Endpoints
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.portfolio_service import PortfolioService
from app.schemas.skill import SkillCategoryRead

router = APIRouter(prefix="/skills", tags=["Skills & Tech Stack"])


@router.get("", response_model=List[SkillCategoryRead], summary="Get Categorized Technical Skills")
def get_skills(db: Session = Depends(get_db)):
    """Retrieve all technical skills organized by category with proficiency ratings and badges."""
    return PortfolioService.get_skill_categories(db)
