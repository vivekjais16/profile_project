"""
Database Models Registry
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from app.models.profile import Profile, CoreCompetency, MetricStat
from app.models.experience import WorkExperience, ExperienceHighlight
from app.models.skill import SkillCategory, Skill
from app.models.project import Project
from app.models.education import Education, Achievement, SoftSkill
from app.models.contact import ContactMessage, AIAgentQuery

__all__ = [
    "Profile",
    "CoreCompetency",
    "MetricStat",
    "WorkExperience",
    "ExperienceHighlight",
    "SkillCategory",
    "Skill",
    "Project",
    "Education",
    "Achievement",
    "SoftSkill",
    "ContactMessage",
    "AIAgentQuery",
]
