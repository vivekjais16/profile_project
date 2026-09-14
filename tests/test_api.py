"""
Comprehensive API & Integration Tests
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from fastapi import status


def test_health_check(client):
    """Verify backend health endpoint responds with online status."""
    response = client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "online"
    assert "Vivek Jaiswal" in data["service"]
    assert data["database"] == "healthy"


def test_render_index_page(client):
    """Verify the root HTML page renders successfully with status 200."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "VIVEK JAISWAL" in response.text
    assert "Senior Software Engineer" in response.text
    assert "FastAPI" in response.text


def test_get_profile(client):
    """Verify profile details match Vivek's resume."""
    response = client.get("/api/v1/profile")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "VIVEK JAISWAL"
    assert data["email"] == "vivekjais16@gmail.com"
    assert data["phone"] == "+91 8920171244"
    assert "Varanasi" in data["location"]
    assert data["years_of_experience"] == 4.5


def test_get_metrics(client):
    """Verify metric stats endpoint returns all 4 key metric cards."""
    response = client.get("/api/v1/profile/metrics")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 4
    labels = [m["label"] for m in data]
    assert "Experience" in labels
    assert "HackerRank" in labels


def test_get_core_competencies(client):
    """Verify all 20 core competencies are returned."""
    response = client.get("/api/v1/profile/competencies")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 20


def test_get_experiences(client):
    """Verify work experiences are returned with bullet points."""
    response = client.get("/api/v1/experiences")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 4
    company_names = [e["company_name"] for e in data]
    assert "Innefu Labs" in company_names
    assert "Shyam Future Tech Pvt. Ltd." in company_names

    # Check Innefu Labs highlights
    innefu = next(e for e in data if e["company_name"] == "Innefu Labs")
    assert innefu["is_current"] is True
    assert len(innefu["highlights"]) > 0


def test_get_skills(client):
    """Verify skills categorized data."""
    response = client.get("/api/v1/skills")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    categories = [c["name"] for c in data]
    assert "Languages" in categories
    assert "Frameworks" in categories
    assert "Generative AI & Agentic AI" in categories


def test_get_projects(client):
    """Verify architectural projects are listed."""
    response = client.get("/api/v1/projects")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 4
    titles = [p["title"] for p in data]
    assert "Autonomous Multi-Agent Orchestrator" in titles
    assert "Custom Model Context Protocol (MCP) Server" in titles


def test_submit_contact_form(client):
    """Verify contact message creation and SQLite persistence."""
    payload = {
        "sender_name": "Google DeepMind Recruiter",
        "sender_email": "recruiter@deepmind.com",
        "subject": "Senior AI Backend Engineer Opportunity",
        "message": "Hi Vivek, we are impressed by your LangGraph and FastAPI experience and would love to speak!",
    }
    response = client.post("/api/v1/contact", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["success"] is True
    assert "safely received" in data["message"]


def test_submit_invalid_contact_form(client):
    """Verify validation error on invalid input."""
    payload = {
        "sender_name": "J",
        "sender_email": "not-an-email",
        "subject": "Hi",
        "message": "Short",
    }
    response = client.post("/api/v1/contact", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_ai_agent_query(client):
    """Verify interactive AI agent query endpoint."""
    payload = {"query": "Tell me about Vivek's LangGraph and Agentic AI work"}
    response = client.post("/api/v1/agent/query", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "Innefu Labs" in data["response"]
    assert "LangGraph" in data["matched_intent"] or "Agentic AI" in data["matched_intent"]
    assert len(data["related_skills"]) > 0


def test_admin_unauthorized_redirect(client):
    """Verify unauthenticated access to /admin redirects to login."""
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code in [status.HTTP_307_TEMPORARY_REDIRECT, status.HTTP_302_FOUND]
    assert "/admin/login" in response.headers.get("location", "")


def test_admin_login_flow(client):
    """Verify successful admin login and dashboard access."""
    # Test valid credentials
    login_data = {
        "username": "vivekjais16",
        "password": "VivekAdmin@2026",
    }
    response = client.post("/admin/login", data=login_data, follow_redirects=False)
    assert response.status_code == status.HTTP_303_SEE_OTHER
    cookie_header = response.headers.get("set-cookie")
    assert "vj_admin_session" in cookie_header

    # Log in client
    client.cookies.set("vj_admin_session", response.cookies["vj_admin_session"])

    # Test accessing protected dashboard
    dash_response = client.get("/admin")
    assert dash_response.status_code == status.HTTP_200_OK
    assert "System & Database Overview" in dash_response.text

    # Test profile update
    profile_data = {
        "full_name": "VIVEK JAISWAL",
        "headline": "Senior Software Engineer — Python | Agentic AI",
        "sub_headline": "Architecting resilient microservices",
        "email": "vivekjais16@gmail.com",
        "phone": "+91 8920171244",
        "location": "Varanasi, UP, India",
        "linkedin_url": "https://www.linkedin.com/in/vivek-jaiswal-979501100/",
        "github_url": "https://github.com/vivekjais16",
        "job_objective": "To architect scalable backend systems",
        "profile_summary_1": "Experienced backend developer",
        "profile_summary_2": "Specialized in Python & LangGraph",
        "years_of_experience": 4.5,
    }
    p_resp = client.post("/admin/profile", data=profile_data)
    assert p_resp.status_code == status.HTTP_200_OK
    assert "Profile details updated successfully!" in p_resp.text

    # Test adding and deleting a project
    new_proj = {
        "title": "Test AI Agent System",
        "tagline": "Real-time AI workflows",
        "category": "Agentic AI",
        "architecture_summary": "Built with FastAPI and Redis",
        "key_features": "Feature 1\nFeature 2",
        "tech_stack": "Python, FastAPI",
        "github_url": "https://github.com/vivekjais16/test",
        "badge": "Testing",
    }
    add_p = client.post("/admin/projects/add", data=new_proj, follow_redirects=False)
    assert add_p.status_code == status.HTTP_303_SEE_OTHER

    # Check project is listed
    proj_view = client.get("/admin/projects")
    assert "Test AI Agent System" in proj_view.text


