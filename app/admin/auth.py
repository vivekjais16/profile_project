"""
Admin Authentication & Session Security Helper
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import hmac
import hashlib
from typing import Optional
from fastapi import Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.admin import AdminUser, hash_password


def generate_session_token(username: str) -> str:
    """Create signed HMAC session token for authenticated admin."""
    secret = settings.SECRET_KEY.encode("utf-8")
    signature = hmac.new(secret, username.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{username}:{signature}"


def verify_session_token(token: str) -> Optional[str]:
    """Verify signed session token and return username if valid."""
    if not token or ":" not in token:
        return None
    username, sig = token.split(":", 1)
    secret = settings.SECRET_KEY.encode("utf-8")
    expected_sig = hmac.new(secret, username.encode("utf-8"), hashlib.sha256).hexdigest()
    if hmac.compare_digest(sig, expected_sig):
        return username
    return None


def get_current_admin(request: Request, db: Session = Depends(get_db)) -> Optional[str]:
    """Dependency extracting and verifying the logged-in admin user from cookies."""
    cookie_token = request.cookies.get(settings.ADMIN_SESSION_COOKIE)
    if not cookie_token:
        return None
    return verify_session_token(cookie_token)


def require_admin(request: Request, db: Session = Depends(get_db)):
    """Enforce authentication on protected admin routes, redirecting unauthenticated users to login."""
    username = get_current_admin(request, db)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/admin/login"},
        )
    return username


def authenticate_admin_user(db: Session, username: str, password: str) -> bool:
    """Verify credentials against SQLite AdminUser table, or fallback to config.py settings."""
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if user:
        return user.verify_password(password)

    # Check against settings fallback
    if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        # Create user entry in SQLite
        new_admin = AdminUser(
            username=settings.ADMIN_USERNAME,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            email=settings.AUTHOR_EMAIL,
        )
        db.add(new_admin)
        db.commit()
        return True

    return False
