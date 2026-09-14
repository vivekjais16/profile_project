"""
Portfolio Data Service
Query layer for profile, experiences, skills, projects, and contact operations.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from app.models.profile import Profile, CoreCompetency, MetricStat
from app.models.experience import WorkExperience
from app.models.skill import SkillCategory, Skill
from app.models.project import Project
from app.models.education import Education, Achievement, SoftSkill
from app.models.contact import ContactMessage
from app.schemas.contact import ContactMessageCreate


class PortfolioService:
    """Service layer coordinating queries and business logic."""

    @staticmethod
    def get_profile(db: Session) -> Optional[Profile]:
        return db.query(Profile).first()

    @staticmethod
    def get_metrics(db: Session) -> List[MetricStat]:
        return db.query(MetricStat).order_by(MetricStat.display_order.asc()).all()

    @staticmethod
    def get_core_competencies(db: Session) -> List[CoreCompetency]:
        return db.query(CoreCompetency).order_by(CoreCompetency.display_order.asc()).all()

    @staticmethod
    def get_experiences(db: Session) -> List[WorkExperience]:
        return (
            db.query(WorkExperience)
            .options(joinedload(WorkExperience.highlights))
            .order_by(WorkExperience.display_order.asc())
            .all()
        )

    @staticmethod
    def get_skill_categories(db: Session) -> List[SkillCategory]:
        return (
            db.query(SkillCategory)
            .options(joinedload(SkillCategory.skills))
            .order_by(SkillCategory.display_order.asc())
            .all()
        )

    @staticmethod
    def get_all_skills(db: Session) -> List[Skill]:
        return db.query(Skill).order_by(Skill.display_order.asc()).all()

    @staticmethod
    def get_projects(db: Session, featured_only: bool = False) -> List[Project]:
        query = db.query(Project)
        if featured_only:
            query = query.filter(Project.featured == True)
        return query.order_by(Project.display_order.asc()).all()

    @staticmethod
    def get_education(db: Session) -> Optional[Education]:
        return db.query(Education).first()

    @staticmethod
    def get_achievements(db: Session) -> List[Achievement]:
        return db.query(Achievement).order_by(Achievement.display_order.asc()).all()

    @staticmethod
    def get_soft_skills(db: Session) -> List[SoftSkill]:
        return db.query(SoftSkill).order_by(SoftSkill.display_order.asc()).all()

    @staticmethod
    def save_contact_message(
        db: Session, message_in: ContactMessageCreate, ip_address: Optional[str] = None
    ) -> ContactMessage:
        msg = ContactMessage(
            sender_name=message_in.sender_name,
            sender_email=message_in.sender_email,
            subject=message_in.subject,
            message=message_in.message,
            ip_address=ip_address,
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def get_portfolio_context(db: Session) -> Dict[str, Any]:
        """Aggregate full data graph for web rendering."""
        profile = PortfolioService.get_profile(db)
        metrics = PortfolioService.get_metrics(db)
        competencies = PortfolioService.get_core_competencies(db)
        experiences = PortfolioService.get_experiences(db)
        skill_categories = PortfolioService.get_skill_categories(db)
        projects = PortfolioService.get_projects(db)
        education = PortfolioService.get_education(db)
        achievements = PortfolioService.get_achievements(db)
        soft_skills = PortfolioService.get_soft_skills(db)

        return {
            "profile": profile,
            "metrics": metrics,
            "competencies": competencies,
            "experiences": experiences,
            "skill_categories": skill_categories,
            "projects": projects,
            "education": education,
            "achievements": achievements,
            "soft_skills": soft_skills,
        }
