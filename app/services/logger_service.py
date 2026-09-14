"""
System Audit & Diagnostic Logging Service
Captures every application event, inquiry, AI query, admin action, and error into SQLite for live diagnostics.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import logging
import traceback
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from app.core.database import SessionLocal
from app.models.admin import SystemLog

logger = logging.getLogger("portfolio.system")


def log_event(
    level: str,
    module: str,
    action: str,
    message: str,
    details: Optional[str] = None,
    ip_address: Optional[str] = None,
) -> None:
    """
    Safely record an event into the SQLite system_logs table and standard logger.
    Guaranteed not to raise exceptions.
    """
    # Also log to Python standard logger
    log_msg = f"[{module.upper()}] {action}: {message}"
    if level.upper() == "ERROR":
        logger.error(log_msg)
    elif level.upper() == "WARNING":
        logger.warning(log_msg)
    else:
        logger.info(log_msg)

    try:
        db = SessionLocal()
        try:
            entry = SystemLog(
                level=level.upper(),
                module=module.upper(),
                action=action,
                message=message,
                details=details,
                ip_address=ip_address,
                timestamp=datetime.now(timezone.utc),
            )
            db.add(entry)
            db.commit()
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Failed to record SystemLog: {e}")


def get_system_logs(
    limit: int = 150,
    level: Optional[str] = None,
    module: Optional[str] = None,
) -> List[SystemLog]:
    """Retrieve system logs ordered by most recent first."""
    db = SessionLocal()
    try:
        query = db.query(SystemLog)
        if level and level.upper() != "ALL":
            query = query.filter(SystemLog.level == level.upper())
        if module and module.upper() != "ALL":
            query = query.filter(SystemLog.module == module.upper())
        return query.order_by(SystemLog.timestamp.desc()).limit(limit).all()
    finally:
        db.close()


def get_log_stats() -> Dict[str, int]:
    """Get count summary of logs by severity."""
    db = SessionLocal()
    try:
        total = db.query(SystemLog).count()
        errors = db.query(SystemLog).filter(SystemLog.level == "ERROR").count()
        warnings = db.query(SystemLog).filter(SystemLog.level == "WARNING").count()
        success = db.query(SystemLog).filter(SystemLog.level == "SUCCESS").count()
        info = db.query(SystemLog).filter(SystemLog.level == "INFO").count()
        return {
            "total": total,
            "errors": errors,
            "warnings": warnings,
            "success": success,
            "info": info,
        }
    finally:
        db.close()


def clear_all_logs() -> bool:
    """Clear all records from system_logs."""
    db = SessionLocal()
    try:
        db.query(SystemLog).delete()
        db.commit()
        log_event("INFO", "SYSTEM", "Logs Cleared", "Admin cleared all system diagnostic logs.")
        return True
    finally:
        db.close()
