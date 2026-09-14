"""
Profile, Core Competencies, and Metric Models
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from app.core.database import Base


class Profile(Base):
    """Core profile information."""
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    headline = Column(String(255), nullable=False)
    sub_headline = Column(String(255), nullable=True)
    email = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    location = Column(String(150), nullable=False)
    linkedin_url = Column(String(255), nullable=False)
    github_url = Column(String(255), nullable=True)
    job_objective = Column(Text, nullable=False)
    profile_summary_1 = Column(Text, nullable=False)
    profile_summary_2 = Column(Text, nullable=False)
    years_of_experience = Column(Float, default=4.5)
    is_available = Column(Boolean, default=True)
    status_text = Column(String(150), default="Available for Senior / Lead Roles")


class CoreCompetency(Base):
    """Core technical competencies highlighted on the portfolio."""
    __tablename__ = "core_competencies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False)
    icon = Column(String(50), default="check-circle")
    display_order = Column(Integer, default=0)


class MetricStat(Base):
    """High-impact statistics shown in the hero/overview section."""
    __tablename__ = "metric_stats"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(100), nullable=False)
    value = Column(String(50), nullable=False)
    subtext = Column(String(150), nullable=True)
    icon = Column(String(50), default="activity")
    display_order = Column(Integer, default=0)
