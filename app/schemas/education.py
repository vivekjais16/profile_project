"""
Education, Achievements, and Soft Skills Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class EducationRead(BaseModel):
    id: int
    degree: str
    field_of_study: str
    institution: str
    location: str
    completion_year: str
    grade: str

    model_config = ConfigDict(from_attributes=True)


class AchievementRead(BaseModel):
    id: int
    title: str
    badge: Optional[str] = None
    description: str
    category: str
    icon: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class SoftSkillRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)
