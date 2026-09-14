"""
Direct Email Notification Service
Sends automated email alerts to Vivek Jaiswal when recruiters submit inquiries.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger("portfolio.email")


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
    if not settings.SMTP_PASSWORD:
        logger.info(
            f"SMTP not configured (SMTP_PASSWORD empty). Message from '{sender_name}' ({sender_email}) "
            f"was safely saved to SQLite database."
        )
        return False

    recipient = settings.NOTIFICATION_EMAIL or settings.AUTHOR_EMAIL

    # Construct Email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚀 [Portfolio Inquiry] {subject} (from {sender_name})"
    msg["From"] = settings.SMTP_USER or settings.AUTHOR_EMAIL
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

    try:
        if settings.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
            server.starttls()

        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"✓ Direct email alert dispatched to {recipient} for message from {sender_name}")
        return True
    except Exception as exc:
        logger.error(f"Failed to dispatch email alert: {exc}")
        return False
