"""
Work Experience Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ExperienceHighlightRead(BaseModel):
    id: int
    bullet_point: str
    highlight_tag: Optional[str] = None
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class WorkExperienceRead(BaseModel):
    id: int
    company_name: str
    parent_group: Optional[str] = None
    designation: str
    employment_type: str
    location: str
    start_date: str
    end_date: str
    is_current: bool
    tech_stack_summary: Optional[str] = None
    display_order: int
    highlights: List[ExperienceHighlightRead] = []

    model_config = ConfigDict(from_attributes=True)
