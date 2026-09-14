"""
Profile and Overview Pydantic Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileRead(BaseModel):
    id: int
    full_name: str
    headline: str
    sub_headline: Optional[str] = None
    email: EmailStr
    phone: str
    location: str
    linkedin_url: str
    github_url: Optional[str] = None
    job_objective: str
    profile_summary_1: str
    profile_summary_2: str
    years_of_experience: float
    is_available: bool
    status_text: str

    model_config = ConfigDict(from_attributes=True)


class CoreCompetencyRead(BaseModel):
    id: int
    title: str
    category: str
    icon: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class MetricStatRead(BaseModel):
    id: int
    label: str
    value: str
    subtext: Optional[str] = None
    icon: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)
