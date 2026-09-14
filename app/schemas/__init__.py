"""
Pydantic Schemas Registry
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from app.schemas.profile import ProfileRead, CoreCompetencyRead, MetricStatRead
from app.schemas.experience import WorkExperienceRead, ExperienceHighlightRead
from app.schemas.skill import SkillRead, SkillCategoryRead
from app.schemas.project import ProjectRead
from app.schemas.education import EducationRead, AchievementRead, SoftSkillRead
from app.schemas.contact import ContactMessageCreate, ContactMessageRead, ContactMessageResponse
from app.schemas.agent import AIAgentQueryRequest, AIAgentQueryResponse

__all__ = [
    "ProfileRead",
    "CoreCompetencyRead",
    "MetricStatRead",
    "WorkExperienceRead",
    "ExperienceHighlightRead",
    "SkillRead",
    "SkillCategoryRead",
    "ProjectRead",
    "EducationRead",
    "AchievementRead",
    "SoftSkillRead",
    "ContactMessageCreate",
    "ContactMessageRead",
    "ContactMessageResponse",
    "AIAgentQueryRequest",
    "AIAgentQueryResponse",
]
