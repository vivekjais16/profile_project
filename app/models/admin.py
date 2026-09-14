"""
Admin User Model for Dynamic Dashboard Authentication
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import hashlib
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base


def utc_now():
    return datetime.now(timezone.utc)


def hash_password(password: str) -> str:
    """Generate secure SHA-256 hash for admin credentials."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class AdminUser(Base):
    """Admin credentials stored dynamically in SQLite."""
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    def verify_password(self, plain_password: str) -> bool:
        return self.password_hash == hash_password(plain_password)

    def set_password(self, plain_password: str) -> None:
        self.password_hash = hash_password(plain_password)
