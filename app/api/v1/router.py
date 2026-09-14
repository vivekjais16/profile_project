"""
Master API Router v1
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from fastapi import APIRouter
from app.api.v1.endpoints import profile, experience, skills, projects, contact, agent, health

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(profile.router)
api_router.include_router(experience.router)
api_router.include_router(skills.router)
api_router.include_router(projects.router)
api_router.include_router(contact.router)
api_router.include_router(agent.router)
