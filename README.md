# Vivek Jaiswal — Senior Software Engineer Portfolio Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00.svg?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![SQLite](https://img.shields.io/badge/SQLite-WAL_Mode-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![LangGraph](https://img.shields.io/badge/Agentic_AI-LangGraph_%26_MCP-blueviolet.svg?style=flat)](https://github.com/langchain-ai/langgraph)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-Pytest_Passing-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://pytest.org)

An enterprise-grade, high-performance personal portfolio platform and REST API built with **FastAPI**, **SQLAlchemy 2.0**, and **SQLite**, designed to showcase the production architectures, systems, and deep technical competencies of **Vivek Jaiswal**.

---

## 🏛️ System Architecture

The application adopts **Clean Architecture** principles separating domain models, presentation layers, query services, and RESTful API endpoints.

```
┌──────────────────────────────────────────────────────────────┐
│                       Client Layer                           │
│  - Tailwind CSS + Glassmorphism UI                          │
│  - Interactive AI Portfolio Terminal (Fetch API)             │
│  - Dynamic Filterable Skills & Projects Matrix               │
│  - Validated Contact Submission System                       │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTP / JSON
┌──────────────────────────────▼───────────────────────────────┐
│                     FastAPI Gateway Layer                    │
│  - Lifespan Schema Auto-Initialization & Data Seeding        │
│  - Jinja2 Server-Side Rendered View Engine (/)               │
│  - OpenAPI / Swagger UI (/docs, /redoc)                     │
│  - Sub-routers: /profile, /experiences, /skills, /agent...    │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                      Service Layer                           │
│  - PortfolioService (Eager loading, Aggregation)             │
│  - PortfolioAgentService (Intent routing & knowledge match)  │
│  - SeederService (Resume data ingestion)                     │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│               Data Persistence (SQLite + WAL)                │
│  - Write-Ahead Logging (WAL) for concurrent read performance │
│  - Foreign Keys & ACID Guarantees via SQLAlchemy 2.0        │
└──────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Highlights

- **Dynamic SQLite Database**: Every section—Profile, Core Competencies, 4.5+ years of Work Experience, Skills Matrix, Architectural Case Studies, Achievements, and Contact Messages—is stored in and dynamically loaded from SQLite.
- **Interactive AI Portfolio Terminal**: Recruiter-facing interactive assistant endpoint (`POST /api/v1/agent/query`) highlighting Vivek's expertise in **Generative AI, LangGraph, and Model Context Protocol (MCP)**.
- **Executive Dark-Mode Aesthetics**: Sleek cyber-slate visual design with ambient glow effects, responsive navigation, stat counter cards, and smooth interactions.
- **Production RESTful APIs**: Fully documented OpenAPI / Swagger specification accessible at `/docs` and ReDoc at `/redoc`.
- **Author Identity**: Fully attributed and authored by **Vivek Jaiswal** (`vivekjais16@gmail.com`).
- **Production-Grade Git Strategy**: Structured branching with `master` and `development`.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Git

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd profile_project

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Seed Database (Automatic on Startup)
The database auto-populates on first run. To manually seed or re-seed:
```bash
python scripts/seed_db.py --force
```

### 3. Launch Development Server
```bash
python scripts/run_server.py
# or using uvicorn directly:
uvicorn app.main:app --reload --port 8000
```

Visit the application:
- **Web Portfolio**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🐳 Docker Deployment

To build and run using Docker Compose:
```bash
docker compose up --build -d
```
Inspect logs and health:
```bash
docker compose ps
docker compose logs -f
```

---

## 🧪 Running Automated Tests

Run the Pytest suite covering all API endpoints, database interactions, and the AI agent query engine:
```bash
pytest tests/ -v
```

---

## 🌿 Git Branching Strategy & GitHub Deployment

The project follows a standard Git flow:
- **`master`**: Production-ready, stable releases tagged with semantic versioning (`v1.0.0`).
- **`development`**: Feature integration branch.

### Push to GitHub
Use the automated push utility:
```bash
./scripts/push_to_github.sh https://github.com/<your-username>/profile_project.git
```
This pushes both `development` and `master` branches, plus tags, to your remote repository in a single step.

---

## 👤 Author

**Vivek Jaiswal**  
*Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI*  
- **Email**: [vivekjais16@gmail.com](mailto:vivekjais16@gmail.com)  
- **LinkedIn**: [linkedin.com/in/vivek-jaiswal-979501100/](https://www.linkedin.com/in/vivek-jaiswal-979501100/)  
- **GitHub**: [github.com/vivekjais16](https://github.com/vivekjais16)  
- **Phone**:   
- **Location**: New Delhi, India  

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
