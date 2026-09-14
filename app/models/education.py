"""
Education, Certifications, and Achievements Models
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Education(Base):
    """Academic background."""
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    degree = Column(String(150), nullable=False)
    field_of_study = Column(String(150), nullable=False)
    institution = Column(String(200), nullable=False)
    location = Column(String(100), nullable=False)
    completion_year = Column(String(50), nullable=False)
    grade = Column(String(50), nullable=False)


class Achievement(Base):
    """Key career achievements, certifications, and technical milestones."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    badge = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), default="Technical")
    icon = Column(String(50), default="award")
    display_order = Column(Integer, default=0)


class SoftSkill(Base):
    """Core soft skills and leadership traits."""
    __tablename__ = "soft_skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    icon = Column(String(50), default="check")
    display_order = Column(Integer, default=0)
