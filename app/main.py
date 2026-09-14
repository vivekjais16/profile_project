"""
Main FastAPI Application Factory & Lifespan Event Handlers
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings, BASE_DIR
from app.core.database import init_db, SessionLocal, get_db
from app.services.seeder_service import seed_portfolio_data
from app.services.portfolio_service import PortfolioService
from app.api.v1.router import api_router
from app.admin.router import admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager:
    - Automatically builds database schemas
    - Checks and seeds initial profile data if SQLite database is newly created
    """
    # 1. Initialize SQLite database schemas
    init_db()

    # 2. Seed data if needed
    db = SessionLocal()
    try:
        seed_portfolio_data(db)
    finally:
        db.close()

    yield


# FastAPI Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=(
        "Production-grade portfolio and profile API platform designed by Vivek Jaiswal, "
        "Senior Software Engineer specializing in Python, Django, FastAPI, Microservices, and Generative/Agentic AI."
    ),
    contact={
        "name": settings.AUTHOR_NAME,
        "email": settings.AUTHOR_EMAIL,
        "url": settings.AUTHOR_LINKEDIN,
    },
    license_info={
        "name": "MIT License",
    },
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files & Template Engine
static_dir = BASE_DIR / "app" / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates_dir = BASE_DIR / "app" / "templates"
templates_dir.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Include API v1 routes and Web Admin Panel
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(admin_router)


@app.get("/", response_class=HTMLResponse, tags=["Web App"])
async def render_portfolio(request: Request, db: Session = Depends(get_db)):
    """Render the responsive, dynamic single-page portfolio."""
    context = PortfolioService.get_portfolio_context(db)
    context["request"] = request
    context["settings"] = settings
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/resume", tags=["Resume"])
@app.get("/download-resume", tags=["Resume"])
async def download_resume_direct(db: Session = Depends(get_db)):
    """Direct route to download Vivek Jaiswal's authentic resume PDF."""
    from fastapi.responses import FileResponse
    profile = PortfolioService.get_profile(db)
    filename = profile.resume_filename if (profile and profile.resume_filename) else "Vivek_Jaiswal_Resume.pdf"
    file_path = BASE_DIR / "app" / "static" / "resume" / filename

    if not file_path.exists():
        fallback = BASE_DIR / "app" / "static" / "resume" / "Vivek_Jaiswal_Resume.pdf"
        if fallback.exists():
            file_path = fallback
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found")

    return FileResponse(
        path=str(file_path),
        filename="Vivek_Jaiswal_Resume.pdf",
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="Vivek_Jaiswal_Resume.pdf"'},
    )


@app.get("/health", tags=["System Health & Diagnostics"])
async def root_health():
    """Quick root health check."""
    return {"status": "healthy", "service": "Vivek Jaiswal Portfolio Platform"}

