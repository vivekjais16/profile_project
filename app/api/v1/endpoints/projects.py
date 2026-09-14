"""
Projects & Architectural Case Studies API Endpoints
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.portfolio_service import PortfolioService
from app.schemas.project import ProjectRead
from app.schemas.education import EducationRead, AchievementRead, SoftSkillRead

router = APIRouter(tags=["Projects & Qualifications"])


@router.get("/projects", response_model=List[ProjectRead], summary="Get Architectural Projects")
def get_projects(featured_only: bool = Query(False), db: Session = Depends(get_db)):
    """Retrieve featured architectural case studies, LangGraph agent workflows, and distributed pipelines."""
    return PortfolioService.get_projects(db, featured_only=featured_only)


@router.get("/education", response_model=Optional[EducationRead], summary="Get Education Background")
def get_education(db: Session = Depends(get_db)):
    """Retrieve Vivek's formal computer science degree information."""
    return PortfolioService.get_education(db)


@router.get("/achievements", response_model=List[AchievementRead], summary="Get Career Achievements")
def get_achievements(db: Session = Depends(get_db)):
    """Retrieve HackerRank certifications, system design milestones, and AI innovations."""
    return PortfolioService.get_achievements(db)


@router.get("/soft-skills", response_model=List[SoftSkillRead], summary="Get Soft Skills & Leadership")
def get_soft_skills(db: Session = Depends(get_db)):
    """Retrieve leadership and problem-solving soft competencies."""
    return PortfolioService.get_soft_skills(db)
