"""
Contact Inquiries Schemas
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactMessageCreate(BaseModel):
    """Schema for incoming contact message form."""
    sender_name: str = Field(..., min_length=2, max_length=120, description="Your full name")
    sender_email: EmailStr = Field(..., description="Your active email address")
    subject: str = Field(..., min_length=3, max_length=200, description="Subject of your message")
    message: str = Field(..., min_length=10, max_length=5000, description="Detailed message or inquiry")


class ContactMessageRead(BaseModel):
    id: int
    sender_name: str
    sender_email: EmailStr
    subject: str
    message: str
    created_at: datetime
    is_read: bool

    model_config = ConfigDict(from_attributes=True)


class ContactMessageResponse(BaseModel):
    success: bool
    message: str
    inquiry_id: Optional[int] = None
