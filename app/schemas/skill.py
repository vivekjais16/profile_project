"""
Technical Skills Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List
from pydantic import BaseModel, ConfigDict


class SkillRead(BaseModel):
    id: int
    name: str
    proficiency_percentage: int
    level: str
    is_featured: bool
    badge_color: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class SkillCategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    icon: str
    display_order: int
    skills: List[SkillRead] = []

    model_config = ConfigDict(from_attributes=True)
