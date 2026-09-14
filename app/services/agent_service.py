"""
Interactive AI Portfolio Assistant Service
Dynamically synthesizes answers from live database models (Profile, Skills, WorkExperience, Projects, Metrics).
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import Dict, Any, List, Optional
import re
from sqlalchemy.orm import Session
from app.models.contact import AIAgentQuery
from app.models.profile import Profile, MetricStat, CoreCompetency
from app.models.experience import WorkExperience
from app.models.skill import Skill, SkillCategory
from app.models.project import Project


class PortfolioAgentService:
    """Intelligent query processing engine answering recruiter and developer questions dynamically from live DB."""

    @classmethod
    def query(cls, db: Session, user_query: str) -> Dict[str, Any]:
        """Synthesize answers dynamically based on live database records and intent matching."""
        q_lower = user_query.lower()

        # 1. Fetch live database state
        profile = db.query(Profile).first()
        skills: List[Skill] = db.query(Skill).all()
        categories: List[SkillCategory] = db.query(SkillCategory).all()
        experiences: List[WorkExperience] = db.query(WorkExperience).order_by(WorkExperience.display_order).all()
        projects: List[Project] = db.query(Project).order_by(Project.display_order).all()
        metrics: List[MetricStat] = db.query(MetricStat).order_by(MetricStat.display_order).all()
        competencies: List[CoreCompetency] = db.query(CoreCompetency).order_by(CoreCompetency.display_order).all()

        # 2. Extract profile attributes dynamically
        full_name = profile.full_name if profile and profile.full_name else "Vivek Jaiswal"
        headline = profile.headline if profile and profile.headline else "Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI"
        sub_headline = profile.sub_headline if profile and profile.sub_headline else ""
        email = profile.email if profile and profile.email else "vivekjais16@gmail.com"
        phone = profile.phone if profile and profile.phone else "+91 8920171244"
        location = profile.location if profile and profile.location else "Varanasi, UP, India"
        linkedin_url = profile.linkedin_url if profile and profile.linkedin_url else "https://www.linkedin.com/in/vivek-jaiswal-979501100/"
        github_url = profile.github_url if profile and profile.github_url else "https://github.com/vivekjais16"
        job_objective = profile.job_objective if profile and profile.job_objective else ""
        summary1 = profile.profile_summary_1 if profile and profile.profile_summary_1 else ""
        summary2 = profile.profile_summary_2 if profile and profile.profile_summary_2 else ""
        status_text = profile.status_text if profile and profile.status_text else "Available for Senior / Lead Roles"
        resume_filename = profile.resume_filename if profile and profile.resume_filename else "Vivek_Jaiswal_Resume.pdf"

        # Determine dynamic experience string (e.g., "4.5+ Years", "5+ Years")
        if profile and profile.years_of_experience:
            exp_val = f"{profile.years_of_experience:.1f}".rstrip("0").rstrip(".")
            exp_str = f"{exp_val}+ Years"
        else:
            exp_metric = next((m.value for m in metrics if any(w in m.label.lower() or w in m.value.lower() for w in ["exp", "yr", "year"])), None)
            if exp_metric:
                exp_str = exp_metric if "yr" in exp_metric.lower() or "year" in exp_metric.lower() else f"{exp_metric} Years"
            else:
                exp_str = "4.5+ Years"

        # Featured and core skills list
        featured_skills = [s.name for s in skills if s.is_featured]
        all_skill_names = [s.name for s in skills]
        top_skills = featured_skills if featured_skills else all_skill_names[:6]

        action_type: Optional[str] = None
        action_url: Optional[str] = None
        download_filename: Optional[str] = None

        # 3. Intent Detection and Dynamic Synthesis

        # --- A. RESUME / CV INTENT ---
        if any(k in q_lower for k in ["resume", "cv", "download", "curriculum", "biodata", "pdf"]):
            matched_intent = "Resume & Credentials"
            response_text = (
                f"Here is {full_name}'s official PDF resume ({resume_filename}). "
                f"It documents {exp_str} of software engineering experience specializing in {headline}, "
                f"production-grade microservices, and modern Agentic AI workflows."
            )
            action_type = "download_resume"
            action_url = "/api/v1/profile/resume"
            download_filename = resume_filename
            related_skills = top_skills[:6]
            suggested_followups = [
                "Tell me about his work experience",
                "What are his core technical skills?",
                "How can I contact Vivek directly?",
            ]

        # --- B. CONTACT & AVAILABILITY INTENT ---
        elif any(k in q_lower for k in ["contact", "email", "phone", "hire", "reach", "available", "location", "address", "call", "whatsapp"]):
            matched_intent = "Contact & Availability"
            response_text = (
                f"{full_name} is currently {status_text}.\n\n"
                f"• Email: {email}\n"
                f"• Phone: {phone}\n"
                f"• Location: {location}\n"
                f"• LinkedIn: {linkedin_url}\n"
                f"• GitHub: {github_url}"
            )
            related_skills = ["Communication", "Technical Leadership", "System Design"]
            suggested_followups = [
                "Download Vivek's resume",
                "What is his total experience?",
                "Tell me about his architectural projects",
            ]

        # --- C. SPECIFIC TECHNOLOGY & AGENTIC AI QUERIES ---
        elif any(k in q_lower for k in [
            "langgraph", "agent", "agentic", "mcp", "model context protocol", "kafka", "spark", "pyspark",
            "fastapi", "django", "python", "database", "sql", "postgres", "redis", "mongo", "neo4j",
            "elastic", "aws", "docker", "microservice", "rag", "vector", "llm"
        ]):
            # Determine specific title for intent
            if any(k in q_lower for k in ["langgraph", "agent", "agentic"]):
                matched_intent = "LangGraph & Agentic AI Systems"
            elif any(k in q_lower for k in ["mcp", "model context protocol"]):
                matched_intent = "Model Context Protocol (MCP)"
            elif any(k in q_lower for k in ["kafka", "spark", "pyspark", "streaming"]):
                matched_intent = "Distributed Event Streaming (Kafka & Spark)"
            elif any(k in q_lower for k in ["fastapi", "django", "microservice", "backend"]):
                matched_intent = "Backend & Microservices Architecture"
            elif any(k in q_lower for k in ["database", "sql", "postgres", "neo4j", "redis", "mongo"]):
                matched_intent = "Database & High-Performance Storage"
            else:
                matched_intent = f"Technical Expertise: {user_query.strip()}"

            # Query matching skills from DB
            matched_db_skills = [
                s for s in skills
                if any(term in s.name.lower() or (s.category and term in s.category.name.lower()) for term in q_lower.split())
            ]

            # Query matching projects from DB
            matched_projects = [
                p for p in projects
                if any(term in p.title.lower() or term in p.tech_stack.lower() or term in p.architecture_summary.lower() for term in q_lower.split())
            ]

            # Query matching experiences and their highlights from DB
            matched_exps = []
            for e in experiences:
                exp_text = f"{e.company_name} {e.designation} {e.tech_stack_summary or ''} " + " ".join(h.bullet_point for h in e.highlights)
                if any(term in exp_text.lower() for term in q_lower.split()):
                    matched_exps.append(e)

            skill_names = [f"{s.name} ({s.proficiency_percentage}% - {s.level})" for s in matched_db_skills]
            skill_summary = f"Database Skills: {', '.join(skill_names)}." if skill_names else f"Core expertise across {headline}."

            project_summary = ""
            if matched_projects:
                proj_bullets = [f"• **{p.title}**: {p.architecture_summary} (Stack: {p.tech_stack})" for p in matched_projects]
                project_summary = "\n\nDemonstrated in Architectural Projects:\n" + "\n".join(proj_bullets)

            exp_summary = ""
            if matched_exps:
                exp_bullets = []
                for e in matched_exps:
                    hl_bullets = [f"    - {h.bullet_point}" for h in e.highlights if any(term in h.bullet_point.lower() for term in q_lower.split())][:2]
                    hl_text = ("\n" + "\n".join(hl_bullets)) if hl_bullets else ""
                    exp_bullets.append(f"• **{e.company_name}** ({e.designation}, {e.start_date}–{e.end_date}): {e.tech_stack_summary or ''}{hl_text}")
                exp_summary = "\n\nProfessional Experience:\n" + "\n".join(exp_bullets)

            response_text = (
                f"{full_name} has {exp_str} of hands-on expertise with these technologies.\n\n"
                f"{skill_summary}{project_summary}{exp_summary}"
            )
            related_skills = [s.name for s in matched_db_skills][:6] if matched_db_skills else top_skills[:6]
            suggested_followups = [
                "Download Vivek's resume",
                "What other backend frameworks does he use?",
                "How can I contact Vivek directly?",
            ]

        # --- D. PROJECTS & ARCHITECTURAL CASE STUDIES INTENT ---
        elif any(k in q_lower for k in ["project", "projects", "portfolio", "architecture", "system", "systems", "built"]):
            matched_intent = "Architectural Projects & Systems"
            proj_blocks = []
            for p in projects:
                github_part = f" ([GitHub]({p.github_url}))" if p.github_url else ""
                proj_blocks.append(
                    f"• **{p.title}** ({p.category}){github_part}: {p.tagline}\n"
                    f"  Architecture: {p.architecture_summary}\n"
                    f"  Stack: {p.tech_stack}"
                )
            projects_str = "\n\n".join(proj_blocks) if proj_blocks else "Featured microservices and distributed AI platforms."
            response_text = (
                f"{full_name} has architected and delivered several production-grade systems:\n\n"
                f"{projects_str}"
            )
            related_skills = [p.category for p in projects] + top_skills[:3]
            # Deduplicate skills
            seen = set()
            related_skills = [x for x in related_skills if not (x in seen or seen.add(x))][:6]
            suggested_followups = [
                "Download Vivek's resume",
                "What is his experience with Kafka and PySpark?",
                "How can I contact Vivek?",
            ]

        # --- E. WORK EXPERIENCE & CAREER HISTORY INTENT ---
        elif any(k in q_lower for k in ["experience", "company", "companies", "career", "work", "history", "role", "roles", "innefu", "shyam", "matrix"]):
            matched_intent = "Career & Work Experience"
            exp_blocks = []
            for exp in experiences:
                bullet_str = ""
                if exp.highlights:
                    bullets = [f"  - {h.bullet_point}" for h in exp.highlights[:2]]
                    bullet_str = "\n" + "\n".join(bullets)
                stack_str = f" [Stack: {exp.tech_stack_summary}]" if exp.tech_stack_summary else ""
                exp_blocks.append(
                    f"• {exp.designation} at {exp.company_name} ({exp.start_date} – {exp.end_date}, {exp.location}){stack_str}{bullet_str}"
                )

            work_history_str = "\n\n".join(exp_blocks) if exp_blocks else "Extensive software engineering experience across high-growth tech companies."
            response_text = (
                f"{full_name} brings {exp_str} of software engineering experience.\n\n"
                f"{work_history_str}"
            )
            related_skills = top_skills[:6]
            suggested_followups = [
                "Download Vivek's resume",
                "What projects has he built?",
                "What is his experience with LangGraph and Agentic AI?",
            ]

        # --- F. GENERAL PROFILE OVERVIEW (DYNAMIC FALLBACK) ---
        else:
            matched_intent = "General Profile Overview"
            overview_parts = [
                f"{full_name} is a {headline} with {exp_str} of professional software engineering experience."
            ]
            if summary1:
                overview_parts.append(summary1)
            if summary2:
                overview_parts.append(summary2)
            if job_objective:
                overview_parts.append(job_objective)

            response_text = " ".join(overview_parts)
            related_skills = top_skills[:6]
            suggested_followups = [
                "Download Vivek's resume",
                "Tell me about his LangGraph & Agentic AI projects",
                "What is Vivek's experience with Kafka and PySpark?",
                "How can I contact Vivek?",
            ]

        # 4. Audit log query in SQLite
        log_entry = AIAgentQuery(
            user_query=user_query,
            agent_response=response_text,
            matched_intent=matched_intent,
        )
        db.add(log_entry)
        db.commit()

        # System logger
        from app.services.logger_service import log_event
        log_event(
            level="INFO",
            module="AI_AGENT",
            action="Agent Query Processed",
            message=f"Query: '{user_query}' → Intent: '{matched_intent}'",
            details=f"Response:\n{response_text}",
        )

        return {
            "query": user_query,
            "response": response_text,
            "matched_intent": matched_intent,
            "related_skills": related_skills,
            "confidence": 0.98,
            "suggested_followups": suggested_followups,
            "action_type": action_type,
            "action_url": action_url,
            "download_filename": download_filename,
        }


