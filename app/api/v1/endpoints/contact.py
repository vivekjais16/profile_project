"""
Contact Form & Message Ingestion API Endpoints
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import List
from fastapi import APIRouter, Depends, Request, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.portfolio_service import PortfolioService
from app.services.email_service import send_contact_email_notification
from app.models.contact import ContactMessage
from app.schemas.contact import ContactMessageCreate, ContactMessageRead, ContactMessageResponse

router = APIRouter(prefix="/contact", tags=["Contact & Inquiries"])


@router.post("", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED, summary="Send Contact Message")
def submit_contact_message(
    message_in: ContactMessageCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Store recruiter or collaborator contact inquiry into SQLite database and dispatch direct email alert."""
    client_ip = request.client.host if request.client else None
    msg = PortfolioService.save_contact_message(db, message_in, ip_address=client_ip)

    # Queue direct email alert to Vivek Jaiswal
    background_tasks.add_task(
        send_contact_email_notification,
        sender_name=message_in.sender_name,
        sender_email=message_in.sender_email,
        subject=message_in.subject,
        message=message_in.message,
    )

    return ContactMessageResponse(
        success=True,
        message="Thank you! Your message has been safely received. Vivek will get back to you shortly.",
        inquiry_id=msg.id,
    )


@router.get("/messages", response_model=List[ContactMessageRead], summary="List Inquiries (Admin)")
def list_contact_messages(db: Session = Depends(get_db)):
    """Retrieve all received contact inquiries stored in the database."""
    return db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
