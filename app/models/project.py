"""
Architectural Projects and Case Studies Models
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base


class Project(Base):
    """Architecture highlights, microservices, and AI systems built."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    tagline = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)  # e.g., "Agentic AI", "Microservices", "RAG & Vector DB"
    architecture_summary = Column(Text, nullable=False)
    key_features = Column(Text, nullable=False)  # JSON or newline-separated list
    tech_stack = Column(String(255), nullable=False)
    github_url = Column(String(255), nullable=True)
    live_demo_url = Column(String(255), nullable=True)
    badge = Column(String(50), default="Featured")
    icon = Column(String(50), default="box")
    featured = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
