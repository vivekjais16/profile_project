"""
Work Experience and Career History Models
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class WorkExperience(Base):
    """Professional work history."""
    __tablename__ = "work_experiences"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False)
    parent_group = Column(String(150), nullable=True)
    designation = Column(String(150), nullable=False)
    employment_type = Column(String(50), default="Full-time")
    location = Column(String(100), nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    is_current = Column(Boolean, default=False)
    tech_stack_summary = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)

    # Relationships
    highlights = relationship(
        "ExperienceHighlight",
        back_populates="experience",
        cascade="all, delete-orphan",
        order_by="ExperienceHighlight.display_order",
    )


class ExperienceHighlight(Base):
    """Individual impact bullet points under each role."""
    __tablename__ = "experience_highlights"

    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("work_experiences.id", ondelete="CASCADE"), nullable=False)
    bullet_point = Column(Text, nullable=False)
    highlight_tag = Column(String(100), nullable=True)
    display_order = Column(Integer, default=0)

    # Relationships
    experience = relationship("WorkExperience", back_populates="highlights")
