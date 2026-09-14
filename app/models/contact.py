"""
Contact Messages and Interactive AI Logs Models
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class ContactMessage(Base):
    """Inquiries submitted through the portfolio contact form."""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String(120), nullable=False)
    sender_email = Column(String(150), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    is_read = Column(Boolean, default=False)


class AIAgentQuery(Base):
    """Auditing logs for queries sent to the interactive AI profile assistant."""
    __tablename__ = "ai_agent_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    matched_intent = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=utc_now)
