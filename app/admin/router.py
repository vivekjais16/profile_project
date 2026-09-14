"""
Web Admin Dashboard Controller & View Routes
Allows Vivek Jaiswal to manage every single record in the SQLite database directly from the browser.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from datetime import datetime
from typing import Optional, List
from pathlib import Path
import shutil
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings, BASE_DIR
from app.core.database import get_db
from app.models.profile import Profile, CoreCompetency, MetricStat
from app.models.experience import WorkExperience, ExperienceHighlight
from app.models.skill import SkillCategory, Skill
from app.models.project import Project
from app.models.education import Education, Achievement, SoftSkill
from app.models.contact import ContactMessage, AIAgentQuery
from app.models.admin import AdminUser, SystemSetting, hash_password
from app.services.portfolio_service import PortfolioService
from app.services.seeder_service import seed_portfolio_data
from app.services.email_service import get_effective_smtp_config, send_test_email
from app.admin.auth import (
    generate_session_token,
    get_current_admin,
    require_admin,
    authenticate_admin_user,
)

admin_router = APIRouter(prefix="/admin", tags=["Web Admin Panel"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


# -----------------------------------------------------------------------------
# Authentication Routes
# -----------------------------------------------------------------------------
@admin_router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request, db: Session = Depends(get_db)):
    current = get_current_admin(request, db)
    if current:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(request=request, name="admin/login.html", context={"error": None})


@admin_router.post("/login", response_class=HTMLResponse)
async def admin_login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if authenticate_admin_user(db, username.strip(), password):
        token = generate_session_token(username.strip())
        response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key=settings.ADMIN_SESSION_COOKIE,
            value=token,
            httponly=True,
            max_age=86400 * 7,
            samesite="lax",
        )
        return response

    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={"error": "Invalid username or password. Please try again."},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


@admin_router.get("/logout")
async def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=settings.ADMIN_SESSION_COOKIE)
    return response


# -----------------------------------------------------------------------------
# Main Dashboard & Overview
# -----------------------------------------------------------------------------
@admin_router.get("", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    profile = PortfolioService.get_profile(db)
    exp_count = db.query(WorkExperience).count()
    skills_count = db.query(Skill).count()
    projects_count = db.query(Project).count()
    messages_count = db.query(ContactMessage).count()
    recent_messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).limit(5).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "admin_user": admin_user,
            "profile": profile,
            "exp_count": exp_count,
            "skills_count": skills_count,
            "projects_count": projects_count,
            "messages_count": messages_count,
            "recent_messages": recent_messages,
        },
    )


# -----------------------------------------------------------------------------
# Profile, Metrics & Competencies Management
# -----------------------------------------------------------------------------
@admin_router.get("/profile", response_class=HTMLResponse)
async def admin_profile_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    profile = PortfolioService.get_profile(db)
    metrics = PortfolioService.get_metrics(db)
    competencies = PortfolioService.get_core_competencies(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/profile.html",
        context={
            "admin_user": admin_user,
            "profile": profile,
            "metrics": metrics,
            "competencies": competencies,
            "msg": None,
        },
    )


@admin_router.post("/profile", response_class=HTMLResponse)
async def admin_profile_save(
    request: Request,
    full_name: str = Form(...),
    headline: str = Form(...),
    sub_headline: str = Form(""),
    email: str = Form(...),
    phone: str = Form(...),
    location: str = Form(...),
    linkedin_url: str = Form(...),
    github_url: str = Form(""),
    job_objective: str = Form(...),
    profile_summary_1: str = Form(...),
    profile_summary_2: str = Form(...),
    years_of_experience: float = Form(4.5),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    profile = PortfolioService.get_profile(db)
    if profile:
        profile.full_name = full_name
        profile.headline = headline
        profile.sub_headline = sub_headline
        profile.email = email
        profile.phone = phone
        profile.location = location
        profile.linkedin_url = linkedin_url
        profile.github_url = github_url
        profile.job_objective = job_objective
        profile.profile_summary_1 = profile_summary_1
        profile.profile_summary_2 = profile_summary_2
        profile.years_of_experience = years_of_experience
        db.commit()

    metrics = PortfolioService.get_metrics(db)
    competencies = PortfolioService.get_core_competencies(db)

    return templates.TemplateResponse(
        request=request,
        name="admin/profile.html",
        context={
            "admin_user": admin_user,
            "profile": profile,
            "metrics": metrics,
            "competencies": competencies,
            "msg": "Profile details updated successfully!",
        },
    )


@admin_router.post("/resume/upload", response_class=HTMLResponse)
async def admin_resume_upload(
    request: Request,
    resume_file: UploadFile = File(...),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    profile = PortfolioService.get_profile(db)
    metrics = PortfolioService.get_metrics(db)
    competencies = PortfolioService.get_core_competencies(db)

    # Validate file format
    if not resume_file.filename.lower().endswith(".pdf"):
        return templates.TemplateResponse(
            request=request,
            name="admin/profile.html",
            context={
                "admin_user": admin_user,
                "profile": profile,
                "metrics": metrics,
                "competencies": competencies,
                "msg": None,
                "resume_err": "Only PDF files (.pdf) are allowed.",
            },
        )

    resume_dir = BASE_DIR / "app" / "static" / "resume"
    resume_dir.mkdir(parents=True, exist_ok=True)
    target_path = resume_dir / "Vivek_Jaiswal_Resume.pdf"

    # Save uploaded file
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(resume_file.file, buffer)

    if profile:
        profile.resume_filename = "Vivek_Jaiswal_Resume.pdf"
        profile.resume_updated_at = datetime.now().strftime("%b %d, %Y - %I:%M %p")
        db.commit()

    return templates.TemplateResponse(
        request=request,
        name="admin/profile.html",
        context={
            "admin_user": admin_user,
            "profile": profile,
            "metrics": metrics,
            "competencies": competencies,
            "msg": f"Resume PDF successfully uploaded ({resume_file.filename}) and active on portfolio!",
            "resume_err": None,
        },
    )


@admin_router.get("/resume/download")
async def admin_resume_download(
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    profile = PortfolioService.get_profile(db)
    filename = profile.resume_filename if (profile and profile.resume_filename) else "Vivek_Jaiswal_Resume.pdf"
    file_path = BASE_DIR / "app" / "static" / "resume" / filename

    if not file_path.exists():
        fallback = BASE_DIR / "app" / "static" / "resume" / "Vivek_Jaiswal_Resume.pdf"
        if fallback.exists():
            file_path = fallback
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume uploaded yet.")

    return FileResponse(
        path=str(file_path),
        filename="Vivek_Jaiswal_Resume.pdf",
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="Vivek_Jaiswal_Resume.pdf"'},
    )



@admin_router.post("/metrics/edit/{metric_id}")
async def admin_metric_edit(
    metric_id: int,
    value: str = Form(...),
    label: str = Form(...),
    subtext: str = Form(""),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    m = db.query(MetricStat).filter(MetricStat.id == metric_id).first()
    if m:
        m.value = value
        m.label = label
        m.subtext = subtext
        db.commit()
    return RedirectResponse(url="/admin/profile", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/competencies/add")
async def admin_competency_add(
    title: str = Form(...),
    category: str = Form(...),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(CoreCompetency).count() + 1
    c = CoreCompetency(title=title, category=category, display_order=order)
    db.add(c)
    db.commit()
    return RedirectResponse(url="/admin/profile", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/competencies/delete/{comp_id}")
async def admin_competency_delete(
    comp_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    c = db.query(CoreCompetency).filter(CoreCompetency.id == comp_id).first()
    if c:
        db.delete(c)
        db.commit()
    return RedirectResponse(url="/admin/profile", status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------------------------------------------------------
# Experiences & Highlights Management
# -----------------------------------------------------------------------------
@admin_router.get("/experiences", response_class=HTMLResponse)
async def admin_experiences_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    experiences = PortfolioService.get_experiences(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/experiences.html",
        context={"admin_user": admin_user, "experiences": experiences, "edit_exp": None},
    )


@admin_router.get("/experiences/edit/{exp_id}", response_class=HTMLResponse)
async def admin_experience_edit_page(
    exp_id: int,
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    experiences = PortfolioService.get_experiences(db)
    edit_exp = db.query(WorkExperience).filter(WorkExperience.id == exp_id).first()
    return templates.TemplateResponse(
        request=request,
        name="admin/experiences.html",
        context={"admin_user": admin_user, "experiences": experiences, "edit_exp": edit_exp},
    )


@admin_router.post("/experiences/add")
async def admin_experience_add(
    company_name: str = Form(...),
    designation: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    location: str = Form(...),
    parent_group: Optional[str] = Form(None),
    tech_stack_summary: Optional[str] = Form(None),
    is_current: bool = Form(False),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    max_order = db.query(WorkExperience).count() + 1
    exp = WorkExperience(
        company_name=company_name,
        parent_group=parent_group,
        designation=designation,
        location=location,
        start_date=start_date,
        end_date=end_date,
        is_current=is_current,
        tech_stack_summary=tech_stack_summary,
        display_order=max_order,
    )
    db.add(exp)
    db.commit()
    return RedirectResponse(url="/admin/experiences", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/experiences/update/{exp_id}")
async def admin_experience_update(
    exp_id: int,
    company_name: str = Form(...),
    designation: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    location: str = Form(...),
    parent_group: Optional[str] = Form(None),
    tech_stack_summary: Optional[str] = Form(None),
    is_current: bool = Form(False),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    exp = db.query(WorkExperience).filter(WorkExperience.id == exp_id).first()
    if exp:
        exp.company_name = company_name
        exp.designation = designation
        exp.start_date = start_date
        exp.end_date = end_date
        exp.location = location
        exp.parent_group = parent_group
        exp.tech_stack_summary = tech_stack_summary
        exp.is_current = is_current
        db.commit()
    return RedirectResponse(url="/admin/experiences", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/experiences/highlight/add/{exp_id}")
async def admin_highlight_add(
    exp_id: int,
    bullet_point: str = Form(...),
    highlight_tag: Optional[str] = Form(None),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(ExperienceHighlight).filter(ExperienceHighlight.experience_id == exp_id).count() + 1
    h = ExperienceHighlight(
        experience_id=exp_id,
        bullet_point=bullet_point,
        highlight_tag=highlight_tag,
        display_order=order,
    )
    db.add(h)
    db.commit()
    return RedirectResponse(url="/admin/experiences", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/experiences/highlight/delete/{highlight_id}")
async def admin_highlight_delete(
    highlight_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    h = db.query(ExperienceHighlight).filter(ExperienceHighlight.id == highlight_id).first()
    if h:
        db.delete(h)
        db.commit()
    return RedirectResponse(url="/admin/experiences", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/experiences/delete/{exp_id}")
async def admin_experience_delete(
    exp_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    exp = db.query(WorkExperience).filter(WorkExperience.id == exp_id).first()
    if exp:
        db.delete(exp)
        db.commit()
    return RedirectResponse(url="/admin/experiences", status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------------------------------------------------------
# Skills Management
# -----------------------------------------------------------------------------
@admin_router.get("/skills", response_class=HTMLResponse)
async def admin_skills_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    categories = PortfolioService.get_skill_categories(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/skills.html",
        context={"admin_user": admin_user, "categories": categories, "edit_skill": None},
    )


@admin_router.get("/skills/edit/{skill_id}", response_class=HTMLResponse)
async def admin_skill_edit_page(
    skill_id: int,
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    categories = PortfolioService.get_skill_categories(db)
    edit_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    return templates.TemplateResponse(
        request=request,
        name="admin/skills.html",
        context={"admin_user": admin_user, "categories": categories, "edit_skill": edit_skill},
    )


@admin_router.post("/skills/add")
async def admin_skill_add(
    name: str = Form(...),
    category_id: int = Form(...),
    proficiency: int = Form(90),
    level: str = Form("Expert"),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    skill = Skill(
        category_id=category_id,
        name=name,
        proficiency_percentage=proficiency,
        level=level,
        is_featured=True,
    )
    db.add(skill)
    db.commit()
    return RedirectResponse(url="/admin/skills", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/skills/update/{skill_id}")
async def admin_skill_update(
    skill_id: int,
    name: str = Form(...),
    category_id: int = Form(...),
    proficiency: int = Form(...),
    level: str = Form(...),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill:
        skill.name = name
        skill.category_id = category_id
        skill.proficiency_percentage = proficiency
        skill.level = level
        db.commit()
    return RedirectResponse(url="/admin/skills", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/skills/delete/{skill_id}")
async def admin_skill_delete(
    skill_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill:
        db.delete(skill)
        db.commit()
    return RedirectResponse(url="/admin/skills", status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------------------------------------------------------
# Projects Management
# -----------------------------------------------------------------------------
@admin_router.get("/projects", response_class=HTMLResponse)
async def admin_projects_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    projects = PortfolioService.get_projects(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/projects.html",
        context={"admin_user": admin_user, "projects": projects, "edit_proj": None},
    )


@admin_router.get("/projects/edit/{project_id}", response_class=HTMLResponse)
async def admin_project_edit_page(
    project_id: int,
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    projects = PortfolioService.get_projects(db)
    edit_proj = db.query(Project).filter(Project.id == project_id).first()
    return templates.TemplateResponse(
        request=request,
        name="admin/projects.html",
        context={"admin_user": admin_user, "projects": projects, "edit_proj": edit_proj},
    )


@admin_router.post("/projects/add")
async def admin_project_add(
    title: str = Form(...),
    tagline: str = Form(...),
    category: str = Form(...),
    architecture_summary: str = Form(...),
    key_features: str = Form(...),
    tech_stack: str = Form(...),
    github_url: Optional[str] = Form(None),
    badge: str = Form("Featured"),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    proj = Project(
        title=title,
        tagline=tagline,
        category=category,
        architecture_summary=architecture_summary,
        key_features=key_features,
        tech_stack=tech_stack,
        github_url=github_url,
        badge=badge,
    )
    db.add(proj)
    db.commit()
    return RedirectResponse(url="/admin/projects", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/projects/update/{project_id}")
async def admin_project_update(
    project_id: int,
    title: str = Form(...),
    tagline: str = Form(...),
    category: str = Form(...),
    architecture_summary: str = Form(...),
    key_features: str = Form(...),
    tech_stack: str = Form(...),
    github_url: Optional[str] = Form(None),
    badge: str = Form("Featured"),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if proj:
        proj.title = title
        proj.tagline = tagline
        proj.category = category
        proj.architecture_summary = architecture_summary
        proj.key_features = key_features
        proj.tech_stack = tech_stack
        proj.github_url = github_url
        proj.badge = badge
        db.commit()
    return RedirectResponse(url="/admin/projects", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/projects/delete/{project_id}")
async def admin_project_delete(
    project_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    proj = db.query(Project).filter(Project.id == project_id).first()
    if proj:
        db.delete(proj)
        db.commit()
    return RedirectResponse(url="/admin/projects", status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------------------------------------------------------
# Education & Achievements Management
# -----------------------------------------------------------------------------
@admin_router.get("/qualifications", response_class=HTMLResponse)
async def admin_qualifications_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    education = PortfolioService.get_education(db)
    achievements = PortfolioService.get_achievements(db)
    soft_skills = PortfolioService.get_soft_skills(db)
    return templates.TemplateResponse(
        request=request,
        name="admin/qualifications.html",
        context={
            "admin_user": admin_user,
            "education": education,
            "achievements": achievements,
            "soft_skills": soft_skills,
            "msg": None,
        },
    )


@admin_router.post("/education/save")
async def admin_education_save(
    degree: str = Form(...),
    field_of_study: str = Form(...),
    institution: str = Form(...),
    location: str = Form(...),
    completion_year: str = Form(...),
    grade: str = Form(...),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    edu = PortfolioService.get_education(db)
    if not edu:
        edu = Education()
        db.add(edu)
    edu.degree = degree
    edu.field_of_study = field_of_study
    edu.institution = institution
    edu.location = location
    edu.completion_year = completion_year
    edu.grade = grade
    db.commit()
    return RedirectResponse(url="/admin/qualifications", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/achievements/add")
async def admin_achievement_add(
    title: str = Form(...),
    badge: str = Form(...),
    description: str = Form(...),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(Achievement).count() + 1
    ach = Achievement(title=title, badge=badge, description=description, display_order=order)
    db.add(ach)
    db.commit()
    return RedirectResponse(url="/admin/qualifications", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/achievements/delete/{ach_id}")
async def admin_achievement_delete(
    ach_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    ach = db.query(Achievement).filter(Achievement.id == ach_id).first()
    if ach:
        db.delete(ach)
        db.commit()
    return RedirectResponse(url="/admin/qualifications", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/soft-skills/add")
async def admin_soft_skill_add(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    icon: str = Form("check"),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(SoftSkill).count() + 1
    sk = SoftSkill(name=name, description=description, icon=icon, display_order=order)
    db.add(sk)
    db.commit()
    return RedirectResponse(url="/admin/qualifications", status_code=status.HTTP_303_SEE_OTHER)


@admin_router.post("/soft-skills/delete/{skill_id}")
async def admin_soft_skill_delete(
    skill_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    sk = db.query(SoftSkill).filter(SoftSkill.id == skill_id).first()
    if sk:
        db.delete(sk)
        db.commit()
    return RedirectResponse(url="/admin/qualifications", status_code=status.HTTP_303_SEE_OTHER)



# -----------------------------------------------------------------------------
# Messages & Inquiries Inbox
# -----------------------------------------------------------------------------
@admin_router.get("/messages", response_class=HTMLResponse)
async def admin_messages_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/messages.html",
        context={"admin_user": admin_user, "messages": messages},
    )


@admin_router.post("/messages/delete/{msg_id}")
async def admin_message_delete(
    msg_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    msg = db.query(ContactMessage).filter(ContactMessage.id == msg_id).first()
    if msg:
        db.delete(msg)
        db.commit()
    return RedirectResponse(url="/admin/messages", status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------------------------------------------------------
# Admin Settings & Credentials Management
# -----------------------------------------------------------------------------
@admin_router.get("/settings", response_class=HTMLResponse)
async def admin_settings_view(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(AdminUser).filter(AdminUser.username == admin_user).first()
    smtp_cfg = get_effective_smtp_config()
    return templates.TemplateResponse(
        request=request,
        name="admin/settings.html",
        context={
            "admin_user": admin_user,
            "user": user,
            "settings": settings,
            "smtp_cfg": smtp_cfg,
            "msg": None,
            "err": None,
        },
    )


@admin_router.post("/settings/credentials", response_class=HTMLResponse)
async def admin_update_credentials(
    request: Request,
    new_username: str = Form(...),
    new_password: Optional[str] = Form(None),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(AdminUser).filter(AdminUser.username == admin_user).first()
    if not user:
        user = AdminUser(
            username=new_username.strip(),
            password_hash=hash_password(settings.ADMIN_PASSWORD),
        )
        db.add(user)

    user.username = new_username.strip()
    if new_password and new_password.strip():
        user.set_password(new_password.strip())

    db.commit()

    token = generate_session_token(user.username)
    smtp_cfg = get_effective_smtp_config()
    response = templates.TemplateResponse(
        request=request,
        name="admin/settings.html",
        context={
            "admin_user": user.username,
            "user": user,
            "settings": settings,
            "smtp_cfg": smtp_cfg,
            "msg": "Credentials updated successfully! Use your new credentials for future logins.",
            "err": None,
        },
    )
    response.set_cookie(
        key=settings.ADMIN_SESSION_COOKIE,
        value=token,
        httponly=True,
        max_age=86400 * 7,
        samesite="lax",
    )
    return response


@admin_router.post("/settings/smtp", response_class=HTMLResponse)
async def admin_update_smtp(
    request: Request,
    smtp_user: str = Form(...),
    smtp_password: str = Form(""),
    notification_email: str = Form(...),
    smtp_host: str = Form("smtp.gmail.com"),
    smtp_port: int = Form(587),
    send_test: Optional[str] = Form(None),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(AdminUser).filter(AdminUser.username == admin_user).first()

    # Upsert settings into SystemSetting table
    def upsert_setting(k: str, v: str, desc: str = ""):
        s = db.query(SystemSetting).filter(SystemSetting.key == k).first()
        if not s:
            s = SystemSetting(key=k, value=v, description=desc)
            db.add(s)
        else:
            s.value = v

    upsert_setting("SMTP_USER", smtp_user.strip(), "SMTP Username / Gmail address")
    if smtp_password and smtp_password.strip():
        upsert_setting("SMTP_PASSWORD", smtp_password.strip(), "Google 16-character App Password")
    upsert_setting("NOTIFICATION_EMAIL", notification_email.strip(), "Inquiry notification recipient")
    upsert_setting("SMTP_HOST", smtp_host.strip(), "SMTP server host")
    upsert_setting("SMTP_PORT", str(smtp_port), "SMTP port")
    db.commit()

    smtp_cfg = get_effective_smtp_config()
    msg = None
    err = None

    if send_test or (smtp_password and smtp_password.strip()):
        pw_to_test = smtp_cfg["smtp_password"]
        success, test_res = send_test_email(
            smtp_host=smtp_cfg["smtp_host"],
            smtp_port=smtp_cfg["smtp_port"],
            smtp_user=smtp_cfg["smtp_user"],
            smtp_password=pw_to_test,
            recipient=smtp_cfg["notification_email"],
        )
        if success:
            msg = f"✅ SMTP Settings saved and test email sent successfully to {smtp_cfg['notification_email']}!"
        else:
            err = f"⚠️ Settings saved, but test email failed: {test_res}"
    else:
        msg = "SMTP Configuration saved successfully!"

    return templates.TemplateResponse(
        request=request,
        name="admin/settings.html",
        context={
            "admin_user": admin_user,
            "user": user,
            "settings": settings,
            "smtp_cfg": smtp_cfg,
            "msg": msg,
            "err": err,
        },
    )


@admin_router.post("/reseed")
async def admin_reseed_database(
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db),
):
    seed_portfolio_data(db, force=True)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

