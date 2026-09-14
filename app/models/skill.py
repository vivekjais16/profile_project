"""
Technical Skills and Categories Models
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class SkillCategory(Base):
    """Categorization for skills (e.g. Frameworks, Databases, Generative AI)."""
    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    icon = Column(String(50), default="layers")
    display_order = Column(Integer, default=0)

    # Relationships
    skills = relationship(
        "Skill",
        back_populates="category",
        cascade="all, delete-orphan",
        order_by="Skill.display_order",
    )


class Skill(Base):
    """Individual technical skill, proficiency, and badges."""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("skill_categories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    proficiency_percentage = Column(Integer, default=90)
    level = Column(String(50), default="Expert")
    is_featured = Column(Boolean, default=False)
    badge_color = Column(String(50), default="indigo")
    display_order = Column(Integer, default=0)

    # Relationships
    category = relationship("SkillCategory", back_populates="skills")
