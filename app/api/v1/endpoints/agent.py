"""
Interactive AI Portfolio Assistant API Endpoint
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.agent_service import PortfolioAgentService
from app.schemas.agent import AIAgentQueryRequest, AIAgentQueryResponse

router = APIRouter(prefix="/agent", tags=["AI Portfolio Assistant"])


@router.post("/query", response_model=AIAgentQueryResponse, status_code=status.HTTP_200_OK, summary="Query Vivek's AI Profile Assistant")
def ask_portfolio_agent(
    payload: AIAgentQueryRequest,
    db: Session = Depends(get_db),
):
    """
    Intelligent AI Assistant Endpoint.
    Demonstrates LangGraph & MCP principles by processing recruiter/visitor queries against Vivek's profile database.
    """
    return PortfolioAgentService.query(db, payload.query)
