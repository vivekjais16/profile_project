"""
Architectural Projects Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ProjectRead(BaseModel):
    id: int
    title: str
    tagline: str
    category: str
    architecture_summary: str
    key_features: str
    tech_stack: str
    github_url: Optional[str] = None
    live_demo_url: Optional[str] = None
    badge: str
    icon: str
    featured: bool
    display_order: int

    model_config = ConfigDict(from_attributes=True)
