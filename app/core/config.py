"""
Core Application Configuration
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application runtime and security settings."""

    # Project metadata
    PROJECT_NAME: str = "Vivek Jaiswal — Senior Software Engineer Portfolio"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Security & CORS
    SECRET_KEY: str = "production-secret-key-vivek-jaiswal-portfolio-2026"
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["*"]

    # Database Configuration (SQLite with WAL mode)
    DATA_DIR: Path = BASE_DIR / "data"
    DATABASE_URL: str = f"sqlite:///{DATA_DIR / 'portfolio.db'}"

    # Profile Metadata
    AUTHOR_NAME: str = "Vivek Jaiswal"
    AUTHOR_EMAIL: str = "vivekjais16@gmail.com"
    AUTHOR_PHONE: str = "+91 8920171244"
    AUTHOR_LINKEDIN: str = "https://www.linkedin.com/in/vivek-jaiswal-979501100/"
    AUTHOR_LOCATION: str = "Varanasi – 221001, Uttar Pradesh, India"
    AUTHOR_GITHUB: str = "https://github.com/vivekjais16"

    # Admin Panel Credentials & Session
    ADMIN_USERNAME: str = "vivekjais16"
    ADMIN_PASSWORD: str = "VivekAdmin@2026"
    ADMIN_SESSION_COOKIE: str = "vj_admin_session"

    # SMTP Direct Email Notification Settings
    SMTP_ENABLED: bool = False
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "vivekjais16@gmail.com"
    SMTP_PASSWORD: str = ""
    NOTIFICATION_EMAIL: str = "vivekjais16@gmail.com"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow",
    )


settings = Settings()
