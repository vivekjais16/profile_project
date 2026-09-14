"""
Interactive AI Portfolio Assistant Service
Demonstrates Vivek Jaiswal's Generative AI, Agentic Workflows & Model Context Protocol expertise.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.contact import AIAgentQuery
from app.models.profile import Profile
from app.models.experience import WorkExperience
from app.models.skill import Skill
from app.models.project import Project


class PortfolioAgentService:
    """Intelligent query processing engine answering recruiter and developer questions."""

    KNOWLEDGE_BASE = {
        "langgraph": {
            "intent": "Agentic AI & LangGraph",
            "summary": (
                "Vivek is actively building autonomous AI Agents using LangGraph at Innefu Labs. "
                "He coordinates multi-agent teams, manages state transitions, persistent chat memory in Redis/PostgreSQL, "
                "and integrates self-correction reflection loops to validate LLM outputs."
            ),
            "skills": ["LangGraph", "Agentic AI", "LangChain", "LLMOps", "FastAPI"],
            "followups": [
                "How does Vivek implement Model Context Protocol (MCP)?",
                "What is Vivek's experience with RAG and Vector Databases?",
            ],
        },
        "mcp": {
            "intent": "Model Context Protocol (MCP)",
            "summary": (
                "Vivek architects custom Model Context Protocol (MCP) servers connecting LLM agents securely to local data stores, "
                "Neo4j graph databases, and external tool endpoints using FastAPI transports (SSE & JSON-RPC)."
            ),
            "skills": ["Model Context Protocol (MCP)", "FastAPI", "Neo4j", "Pydantic v2", "Docker"],
            "followups": [
                "Tell me about Vivek's LangGraph agent workflows",
                "What are Vivek's core backend frameworks?",
            ],
        },
        "kafka": {
            "intent": "Distributed Event Streaming & Kafka",
            "summary": (
                "At Shyam Future Tech, Vivek built and maintained Apache Kafka with Zookeeper for real-time distributed data "
                "streaming. He coupled Kafka with PySpark to process 100GB+ datasets and Celery for background jobs."
            ),
            "skills": ["Apache Kafka", "Zookeeper", "PySpark", "Redis", "Celery", "AWS"],
            "followups": [
                "What AWS cloud services has Vivek worked with?",
                "Tell me about his microservices experience",
            ],
        },
        "fastapi": {
            "intent": "FastAPI & Async Architecture",
            "summary": (
                "Vivek has extensive experience building high-performance, asynchronous RESTful microservices using FastAPI (async/await), "
                "dependency injection, SQLAlchemy 2.0 connection pooling, Pydantic v2 validation, and OpenAPI documentation."
            ),
            "skills": ["FastAPI", "SQLAlchemy", "Pydantic", "Uvicorn", "AsyncIO", "Docker"],
            "followups": [
                "What is Vivek's experience with Django & DRF?",
                "Show me his database optimization skills",
            ],
        },
        "database": {
            "intent": "Databases & Storage Engines",
            "summary": (
                "Vivek is proficient across relational, graph, document, and vector databases: PostgreSQL, MySQL, SQLite, Neo4j, "
                "MongoDB, Elasticsearch, Redis, and vector stores like FAISS, Chroma, and PGVector. He holds a 5-star HackerRank SQL rating."
            ),
            "skills": ["PostgreSQL", "MySQL", "SQLite", "Neo4j", "Redis", "Elasticsearch", "PGVector"],
            "followups": [
                "What are Vivek's achievements on HackerRank?",
                "How did he use Neo4j and Elasticsearch together?",
            ],
        },
        "experience": {
            "intent": "Career & Experience Overview",
            "summary": (
                "Vivek has 4.5+ years of software engineering experience. He currently serves as Senior Software Engineer at Innefu Labs (Jan'26–Present) "
                "leading AI agents and backend systems. Previously, he was Back-end Developer at Shyam Future Tech (May'22–Dec'25) and "
                "Associate Technical Project Manager at NS Matrix Services (2017)."
            ),
            "skills": ["Python", "FastAPI", "Django", "LangGraph", "Microservices", "System Design"],
            "followups": [
                "What is Vivek's educational background?",
                "Is Vivek currently open to new opportunities?",
            ],
        },
        "contact": {
            "intent": "Contact & Availability",
            "summary": (
                "Vivek Jaiswal is available for Senior and Lead Software Engineer roles. "
                "Email: vivekjais16@gmail.com | Phone: +91 8920171244 | LinkedIn: linkedin.com/in/vivek-jaiswal-979501100/ | Location: Varanasi, UP, India."
            ),
            "skills": ["Communication", "Stakeholder Collaboration", "Technical Leadership"],
            "followups": [
                "Download Vivek's resume",
                "What are his core competencies?",
            ],
            "action_type": None,
            "action_url": None,
        },
        "resume": {
            "intent": "Resume & Credentials",
            "summary": (
                "Here is Vivek Jaiswal's authentic, executive-grade PDF resume. "
                "It covers 4.5+ years of engineering experience across Innefu Labs & Shyam Future Tech, "
                "LangGraph Multi-Agent architectures, Kafka/PySpark streaming pipelines, and full-stack technical competencies."
            ),
            "skills": ["Python", "FastAPI", "Django", "LangGraph", "Kafka", "PostgreSQL"],
            "followups": [
                "What are Vivek's core competencies?",
                "How can I contact Vivek directly?",
            ],
            "action_type": "download_resume",
            "action_url": "/api/v1/profile/resume",
            "download_filename": "Vivek_Jaiswal_Resume.pdf",
        },
    }

    @classmethod
    def query(cls, db: Session, user_query: str) -> Dict[str, Any]:
        """Synthesize answers dynamically based on intent matching against Vivek's profile data."""
        q_lower = user_query.lower()
        matched_key = None

        # Keyword mapping heuristics
        if any(k in q_lower for k in ["resume", "cv", "download", "curriculum", "biodata", "pdf"]):
            matched_key = "resume"
        elif any(k in q_lower for k in ["langgraph", "agent", "swarm", "autonomous", "llm"]):
            matched_key = "langgraph"
        elif any(k in q_lower for k in ["mcp", "model context protocol", "tool"]):
            matched_key = "mcp"
        elif any(k in q_lower for k in ["kafka", "stream", "spark", "pyspark", "event"]):
            matched_key = "kafka"
        elif any(k in q_lower for k in ["fastapi", "async", "rest", "api", "backend"]):
            matched_key = "fastapi"
        elif any(k in q_lower for k in ["db", "database", "sql", "postgres", "neo4j", "elastic", "redis", "mongo", "mysql"]):
            matched_key = "database"
        elif any(k in q_lower for k in ["contact", "email", "phone", "hire", "reach", "available"]):
            matched_key = "contact"
        elif any(k in q_lower for k in ["experience", "company", "innefu", "shyam", "work", "history", "years"]):
            matched_key = "experience"

        action_type = None
        action_url = None
        download_filename = None

        if matched_key and matched_key in cls.KNOWLEDGE_BASE:
            data = cls.KNOWLEDGE_BASE[matched_key]
            response_text = data["summary"]
            intent = data["intent"]
            skills = data["skills"]
            followups = data["followups"]
            action_type = data.get("action_type")
            action_url = data.get("action_url")
            download_filename = data.get("download_filename")
        else:
            # Dynamic fallback: retrieve profile details from DB
            profile = db.query(Profile).first()
            name = profile.full_name if profile else "Vivek Jaiswal"
            obj = profile.job_objective if profile else ""
            response_text = (
                f"{name} is a Senior Software Engineer with 4.5+ years of experience specializing in Python, Django, FastAPI, "
                f"Microservices, and cutting-edge Generative/Agentic AI (LangGraph & MCP). {obj}"
            )
            intent = "General Profile Overview"
            skills = ["Python", "FastAPI", "Django", "LangGraph", "Microservices"]
            followups = [
                "Download Vivek's resume",
                "Tell me about his LangGraph & Agentic AI projects",
                "What is Vivek's experience with Kafka and PySpark?",
                "How can I contact Vivek?",
            ]

        # Audit log in SQLite
        log_entry = AIAgentQuery(
            user_query=user_query,
            agent_response=response_text,
            matched_intent=intent,
        )
        db.add(log_entry)
        db.commit()

        return {
            "query": user_query,
            "response": response_text,
            "matched_intent": intent,
            "related_skills": skills,
            "confidence": 0.98,
            "suggested_followups": followups,
            "action_type": action_type,
            "action_url": action_url,
            "download_filename": download_filename,
        }

