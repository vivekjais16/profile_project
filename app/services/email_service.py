"""
Direct Email Notification Service
Sends automated email alerts to Vivek Jaiswal when recruiters submit inquiries.
Includes IPv4 socket enforcement and automatic TLS/SSL fallback for cloud environments like Render.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import socket
import smtplib
import logging
import traceback
from typing import Tuple, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.admin import SystemSetting
from app.services.logger_service import log_event

logger = logging.getLogger("portfolio.email")


def _get_ipv4_smtp_server(host: str, port: int, timeout: int = 12):
    """
    Creates an SMTP connection with forced IPv4 resolution.
    Fixes '[Errno 101] Network is unreachable' caused by IPv6 DNS resolution in cloud containers.
    """
    orig_getaddrinfo = socket.getaddrinfo

    def forced_ipv4_getaddrinfo(h, p, family=0, sock_type=0, proto=0, flags=0):
        return orig_getaddrinfo(h, p, socket.AF_INET, sock_type, proto, flags)

    socket.getaddrinfo = forced_ipv4_getaddrinfo
    try:
        if port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=timeout)
        else:
            server = smtplib.SMTP(host, port, timeout=timeout)
            server.ehlo()
            server.starttls()
            server.ehlo()
        return server
    finally:
        socket.getaddrinfo = orig_getaddrinfo


def _establish_smtp_connection(host: str, port: int, user: str, password: str, timeout: int = 12):
    """
    Attempts connection on specified port with automatic fallback between Port 587 (TLS) and Port 465 (SSL).
    """
    clean_password = password.replace(" ", "").strip()
    errors = []

    # Attempt 1: Requested port
    try:
        server = _get_ipv4_smtp_server(host, port, timeout=timeout)
        server.login(user, clean_password)
        return server, port, None
    except Exception as e:
        errors.append(f"Port {port}: {str(e)}")

    # Attempt 2: Fallback port (switch 587 <-> 465)
    fallback_port = 465 if port != 465 else 587
    try:
        server = _get_ipv4_smtp_server(host, fallback_port, timeout=timeout)
        server.login(user, clean_password)
        return server, fallback_port, None
    except Exception as e:
        errors.append(f"Fallback Port {fallback_port}: {str(e)}")

    return None, port, " | ".join(errors)


def get_effective_smtp_config() -> Dict[str, Any]:
    """Retrieve active SMTP credentials from SQLite with fallback to environment/settings."""
    config = {
        "smtp_host": settings.SMTP_HOST or "smtp.gmail.com",
        "smtp_port": settings.SMTP_PORT or 587,
        "smtp_user": settings.SMTP_USER or "vivekjais16@gmail.com",
        "smtp_password": settings.SMTP_PASSWORD or "",
        "notification_email": settings.NOTIFICATION_EMAIL or settings.AUTHOR_EMAIL or "vivekjais16@gmail.com",
    }

    try:
        db = SessionLocal()
        try:
            settings_rows = db.query(SystemSetting).all()
            for row in settings_rows:
                if row.key == "SMTP_HOST" and row.value:
                    config["smtp_host"] = row.value
                elif row.key == "SMTP_PORT" and row.value:
                    config["smtp_port"] = int(row.value)
                elif row.key == "SMTP_USER" and row.value:
                    config["smtp_user"] = row.value
                elif row.key == "SMTP_PASSWORD" and row.value:
                    config["smtp_password"] = row.value
                elif row.key == "NOTIFICATION_EMAIL" and row.value:
                    config["notification_email"] = row.value
        finally:
            db.close()
    except Exception as e:
        logger.debug(f"Could not read SystemSetting from DB: {e}")

    return config


def send_test_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    recipient: str,
) -> Tuple[bool, str]:
    """Sends a verification email to test SMTP connectivity and credentials."""
    if not smtp_password or not smtp_password.strip():
        return False, "SMTP Password is empty. Please enter your 16-character Google App Password."

    clean_password = smtp_password.replace(" ", "").strip()
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "✅ [FastAPI Portfolio] SMTP Email Notification Test Successful!"
    msg["From"] = smtp_user
    msg["To"] = recipient

    body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 24px;">
        <div style="max-width: 550px; margin: 0 auto; background: #1e293b; border: 1px solid #10b981; border-radius: 12px; padding: 24px;">
            <h2 style="color: #10b981; margin-top: 0;">🚀 Direct Email Forwarding Active</h2>
            <p>Hi Vivek,</p>
            <p>Your FastAPI portfolio email forwarding system is now <strong>100% connected and operational</strong>.</p>
            <p>Whenever a recruiter or hiring manager submits a message on your portfolio, it will be delivered directly to this inbox (<strong>{recipient}</strong>) in real time.</p>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 20px 0;">
            <p style="font-size: 12px; color: #94a3b8;">Sent via FastAPI • SQLAlchemy 2.0 • Render Cloud Production Engine</p>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, "html"))

    server, connected_port, error_msg = _establish_smtp_connection(
        host=smtp_host,
        port=smtp_port,
        user=smtp_user,
        password=clean_password,
        timeout=15,
    )

    if not server:
        err_detail = f"Failed connecting to {smtp_host} on port {smtp_port} & fallback. Details: {error_msg}"
        log_event(
            level="ERROR",
            module="EMAIL",
            action="SMTP Test Email Failed",
            message=f"Could not connect to {smtp_host}: {error_msg}",
            details=err_detail,
        )
        return False, f"SMTP Connection Failed: {error_msg}"

    try:
        server.send_message(msg)
        server.quit()
        log_event(
            level="SUCCESS",
            module="EMAIL",
            action="SMTP Test Email Dispatched",
            message=f"Test email successfully sent to {recipient} via port {connected_port}",
        )
        return True, f"Test email successfully delivered to {recipient} (via Port {connected_port})! Check your inbox."
    except Exception as exc:
        log_event(
            level="ERROR",
            module="EMAIL",
            action="SMTP Send Error",
            message=f"Error sending message payload: {str(exc)}",
            details=traceback.format_exc(),
        )
        return False, f"Failed to send test email payload: {str(exc)}"


def send_contact_email_notification(
    sender_name: str,
    sender_email: str,
    subject: str,
    message: str,
) -> bool:
    """
    Sends an instant email alert to Vivek Jaiswal's personal email when a new inquiry arrives.
    Executed asynchronously in a background task.
    """
    cfg = get_effective_smtp_config()
    smtp_password = cfg["smtp_password"].replace(" ", "").strip() if cfg["smtp_password"] else ""

    if not smtp_password:
        log_event(
            level="WARNING",
            module="EMAIL",
            action="Email Notification Skipped",
            message=f"Inquiry from '{sender_name}' ({sender_email}) saved to DB, but SMTP_PASSWORD is not set.",
        )
        return False

    recipient = cfg["notification_email"]
    smtp_user = cfg["smtp_user"]
    smtp_host = cfg["smtp_host"]
    smtp_port = cfg["smtp_port"]

    # Construct Email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚀 [Portfolio Inquiry] {subject} (from {sender_name})"
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg["Reply-To"] = sender_email

    # Plain text version
    text_content = f"""
New Inquiry Received from Portfolio:
------------------------------------
From: {sender_name} <{sender_email}>
Subject: {subject}
Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

Message:
{message}

------------------------------------
You can reply directly to this email to reach {sender_name}.
"""

    # Rich HTML version
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
            .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; max-width: 600px; margin: 0 auto; }}
            .badge {{ background: #10b981; color: #022c22; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }}
            .field {{ margin-bottom: 12px; }}
            .label {{ color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .value {{ color: #ffffff; font-size: 15px; font-weight: 600; }}
            .message-box {{ background: #0b0f19; border-left: 4px solid #6366f1; padding: 16px; border-radius: 6px; margin-top: 16px; font-size: 14px; line-height: 1.6; color: #e2e8f0; }}
            .btn {{ display: inline-block; background: #6366f1; color: #ffffff !important; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <span class="badge">NEW PORTFOLIO INQUIRY</span>
                <span style="color: #64748b; font-size: 12px;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</span>
            </div>
            <div class="field">
                <div class="label">Sender Name</div>
                <div class="value">{sender_name}</div>
            </div>
            <div class="field">
                <div class="label">Sender Email</div>
                <div class="value"><a href="mailto:{sender_email}" style="color: #38bdf8;">{sender_email}</a></div>
            </div>
            <div class="field">
                <div class="label">Subject</div>
                <div class="value">{subject}</div>
            </div>
            <div class="field">
                <div class="label">Message</div>
                <div class="message-box">{message.replace(chr(10), '<br>')}</div>
            </div>
            <a href="mailto:{sender_email}?subject=Re: {subject}" class="btn">Reply to {sender_name}</a>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    server, connected_port, error_msg = _establish_smtp_connection(
        host=smtp_host,
        port=smtp_port,
        user=smtp_user,
        password=smtp_password,
        timeout=15,
    )

    if not server:
        log_event(
            level="ERROR",
            module="EMAIL",
            action="Inquiry Email Dispatch Failed",
            message=f"Could not connect to SMTP server: {error_msg}",
            details=f"Sender: {sender_name} <{sender_email}>\nSubject: {subject}\nError: {error_msg}",
        )
        return False

    try:
        server.send_message(msg)
        server.quit()
        log_event(
            level="SUCCESS",
            module="EMAIL",
            action="Inquiry Email Delivered",
            message=f"Forwarded inquiry from '{sender_name}' ({sender_email}) to {recipient} via port {connected_port}",
        )
        return True
    except Exception as exc:
        log_event(
            level="ERROR",
            module="EMAIL",
            action="Inquiry Email Send Error",
            message=f"Error sending inquiry email: {str(exc)}",
            details=traceback.format_exc(),
        )
        return False
