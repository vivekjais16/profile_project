"""
Interactive AI Portfolio Assistant Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AIAgentQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500, description="Question about Vivek's experience, stack, or projects")


class AIAgentQueryResponse(BaseModel):
    query: str
    response: str
    matched_intent: str
    related_skills: List[str] = []
    confidence: float = 0.98
    suggested_followups: List[str] = []
    action_type: Optional[str] = None
    action_url: Optional[str] = None
    download_filename: Optional[str] = None

