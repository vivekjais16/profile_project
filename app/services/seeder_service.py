"""
Database Seeder Service
Populates SQLite with Vivek Jaiswal's full resume data.
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from sqlalchemy.orm import Session
from app.models.profile import Profile, CoreCompetency, MetricStat
from app.models.experience import WorkExperience, ExperienceHighlight
from app.models.skill import SkillCategory, Skill
from app.models.project import Project
from app.models.education import Education, Achievement, SoftSkill


def seed_portfolio_data(db: Session, force: bool = False) -> None:
    """Populate database with complete resume and profile data."""
    existing_profile = db.query(Profile).first()
    if existing_profile and not force:
        return

    if force:
        db.query(ExperienceHighlight).delete()
        db.query(WorkExperience).delete()
        db.query(Skill).delete()
        db.query(SkillCategory).delete()
        db.query(Project).delete()
        db.query(Achievement).delete()
        db.query(Education).delete()
        db.query(SoftSkill).delete()
        db.query(CoreCompetency).delete()
        db.query(MetricStat).delete()
        db.query(Profile).delete()
        db.commit()

    # 1. Profile Core
    profile = Profile(
        full_name="VIVEK JAISWAL",
        headline="Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI",
        sub_headline="Architecting resilient microservices, autonomous LLM agents (LangGraph), and high-throughput data platforms",
        email="vivekjais16@gmail.com",
        phone="+91 8920171244",
        location="Varanasi – 221001, Uttar Pradesh, India",
        linkedin_url="https://linkedin.com/in/vivek-jaiswal",
        github_url="https://github.com/vivekjaiswal",
        job_objective=(
            "Driving the development of scalable, AI-powered, and high-performance applications by leveraging 4.5+ years of "
            "expertise in Python, Django, FastAPI, Flask, Machine Learning, NLP, Generative AI, and Agentic AI technologies. "
            "Seeking a Senior/Lead Software Engineer role to contribute to intelligent backend systems, autonomous LLM agents, "
            "LangGraph workflows, Model Context Protocol (MCP) servers, and enterprise-scale, cloud-native data platforms."
        ),
        profile_summary_1=(
            "Results-driven Senior Software Engineer with 4.5+ years of experience designing scalable backend systems and "
            "AI-powered applications using Python, Django, DRF, FastAPI, and Flask. Strong expertise in Microservices "
            "Architecture, Distributed Systems, Asynchronous processing, System Design, and cloud-native backend development, "
            "with hands-on experience integrating Machine Learning, Generative AI, and Agentic AI solutions into enterprise applications."
        ),
        profile_summary_2=(
            "Experienced in designing and deploying NLP and LLM-powered systems using Hugging Face Transformers, LangChain, "
            "LangGraph, Model Context Protocol (MCP), Retrieval-Augmented Generation (RAG), Prompt Engineering, Semantic Search, "
            "and Vector Embeddings, with working exposure to LLMOps for deploying and monitoring LLM-driven services. "
            "Strong experience in Data Engineering using PySpark, Kafka, Redis, and Elasticsearch, with hands-on expertise in AWS, "
            "Docker, Kubernetes, Neo4j, TensorFlow, and MLOps workflows for production-grade AI systems."
        ),
        years_of_experience=4.5,
        is_available=True,
        status_text="Available for Senior / Lead Backend & AI Roles",
    )
    db.add(profile)

    # 2. Metric Statistics
    metrics = [
        MetricStat(label="Experience", value="4.5+ Yrs", subtext="Backend & AI Engineering", icon="calendar", display_order=1),
        MetricStat(label="AWS Uptime", value="99.9%", subtext="Cloud-Native SLA Achieved", icon="server", display_order=2),
        MetricStat(label="Data Ingestion", value="100GB+", subtext="Distributed Spark & Kafka", icon="database", display_order=3),
        MetricStat(label="HackerRank", value="5-Star", subtext="Python & SQL Certified", icon="award", display_order=4),
    ]
    db.add_all(metrics)

    # 3. Core Competencies
    competencies_data = [
        ("Python, Django, FastAPI & Flask Development", "Core Backend", "code", 1),
        ("Agentic AI & Multi-Agent Workflows (LangGraph)", "AI & Agents", "bot", 2),
        ("RESTful & Async API Design", "Core Backend", "globe", 3),
        ("Model Context Protocol (MCP) Integration & Custom Servers", "AI & Agents", "cpu", 4),
        ("Generative AI, LLMs, LangChain & LLMOps", "AI & Agents", "sparkles", 5),
        ("Retrieval-Augmented Generation (RAG) & Vector Databases", "AI & Agents", "search", 6),
        ("Microservices Architecture & System Design (HLD/LLD)", "Architecture", "layout", 7),
        ("Event-Driven Systems & Messaging (Kafka)", "Distributed Systems", "git-branch", 8),
        ("Database Design & Query Optimization (ORMs)", "Data & Storage", "database", 9),
        ("Distributed Systems & High-Availability Architecture", "Architecture", "network", 10),
        ("Asynchronous & Concurrent Systems", "Core Backend", "zap", 11),
        ("Caching & Performance Tuning (Redis)", "Data & Storage", "hard-drive", 12),
        ("Background Jobs & Workflow Orchestration (Celery)", "Core Backend", "clock", 13),
        ("Cloud-Native & Containerized Deployments (Docker/K8s)", "DevOps & Cloud", "box", 14),
        ("DevOps, CI/CD & Infrastructure Automation", "DevOps & Cloud", "tool", 15),
        ("Unit Testing & TDD (Pytest)", "Testing & Quality", "check-square", 16),
        ("Machine Learning Integration in APIs", "AI & Agents", "terminal", 17),
        ("Graph Databases & Knowledge Graph Modeling (Neo4j)", "Data & Storage", "share-2", 18),
        ("Full-Text Search & Index Tuning (Elasticsearch)", "Data & Storage", "file-text", 19),
        ("ETL Pipeline Design & Data Engineering", "Data & Storage", "refresh-cw", 20),
    ]
    for title, cat, icon, order in competencies_data:
        db.add(CoreCompetency(title=title, category=cat, icon=icon, display_order=order))

    # 4. Technical Skills by Category
    categories_skills = [
        (
            "Languages", "languages", "code", 1,
            [
                ("Python", 95, "Expert", True, "emerald"),
            ]
        ),
        (
            "Frameworks", "frameworks", "layers", 2,
            [
                ("FastAPI", 95, "Expert", True, "emerald"),
                ("Django", 95, "Expert", True, "emerald"),
                ("Django REST Framework (DRF)", 92, "Expert", True, "emerald"),
                ("Flask", 90, "Advanced", True, "teal"),
                ("SQLAlchemy", 92, "Expert", True, "teal"),
                ("Celery", 90, "Advanced", True, "teal"),
                ("LangChain", 92, "Expert", True, "indigo"),
                ("LangGraph", 90, "Advanced", True, "indigo"),
                ("Hugging Face Transformers", 88, "Advanced", True, "indigo"),
            ]
        ),
        (
            "Generative AI & Agentic AI", "generative-ai", "bot", 3,
            [
                ("Agentic AI", 92, "Expert", True, "indigo"),
                ("LangGraph Multi-Agent Workflows", 90, "Advanced", True, "indigo"),
                ("Model Context Protocol (MCP)", 92, "Expert", True, "indigo"),
                ("Generative AI & LLMs", 94, "Expert", True, "indigo"),
                ("Retrieval-Augmented Generation (RAG)", 92, "Expert", True, "indigo"),
                ("Prompt Engineering", 90, "Advanced", True, "indigo"),
                ("NLP Pipelines", 88, "Advanced", False, "indigo"),
                ("AI Agents & Conversational AI", 90, "Advanced", True, "indigo"),
                ("Document Processing", 88, "Advanced", False, "indigo"),
                ("LLMOps", 85, "Advanced", False, "indigo"),
            ]
        ),
        (
            "Databases & Storage", "databases", "database", 4,
            [
                ("PostgreSQL", 92, "Expert", True, "cyan"),
                ("MySQL", 90, "Advanced", True, "cyan"),
                ("SQLite", 95, "Expert", True, "cyan"),
                ("MongoDB", 85, "Advanced", False, "cyan"),
                ("Neo4j (Graph DB)", 88, "Advanced", True, "cyan"),
                ("Query Optimization & Indexing", 94, "Expert", True, "cyan"),
            ]
        ),
        (
            "Messaging & Distributed Systems", "messaging-distributed", "radio", 5,
            [
                ("Redis (Caching & Queues)", 92, "Expert", True, "rose"),
                ("Apache Kafka", 90, "Advanced", True, "rose"),
                ("Zookeeper", 85, "Proficient", False, "rose"),
                ("Apache Spark (PySpark)", 88, "Advanced", True, "rose"),
            ]
        ),
        (
            "Search & Vector Platforms", "search-vector", "search", 6,
            [
                ("Elasticsearch", 90, "Advanced", True, "amber"),
                ("Semantic Search", 92, "Expert", True, "amber"),
                ("Text Embeddings", 90, "Advanced", True, "amber"),
                ("Vector Databases (FAISS, Chroma, PGVector)", 90, "Advanced", True, "amber"),
            ]
        ),
        (
            "ML & Data Science", "ml-datascience", "cpu", 7,
            [
                ("Machine Learning & Deep Learning", 88, "Advanced", True, "purple"),
                ("TensorFlow", 85, "Advanced", False, "purple"),
                ("Pandas & NumPy", 92, "Expert", True, "purple"),
                ("OpenCV & DeepFace", 86, "Advanced", False, "purple"),
                ("ETL Pipelines", 90, "Advanced", True, "purple"),
            ]
        ),
        (
            "DevOps & Cloud", "devops-cloud", "cloud", 8,
            [
                ("Docker & Containerization", 92, "Expert", True, "sky"),
                ("Kubernetes (K8s)", 85, "Advanced", True, "sky"),
                ("AWS (EC2, S3, Lambda, RDS, SQS, SNS, ECS, ECR)", 90, "Advanced", True, "sky"),
                ("CI/CD Automation", 88, "Advanced", False, "sky"),
            ]
        ),
        (
            "Testing, Tools & Architecture", "testing-architecture", "check-circle", 9,
            [
                ("REST API Design & OpenAPI", 96, "Expert", True, "green"),
                ("Microservices Architecture (HLD/LLD)", 92, "Expert", True, "green"),
                ("Pytest & Unit Testing (TDD)", 92, "Expert", True, "green"),
                ("Postman & Swagger", 95, "Expert", False, "green"),
                ("Git & Version Control", 94, "Expert", True, "green"),
            ]
        ),
    ]

    for cat_name, cat_slug, cat_icon, cat_order, skills_list in categories_skills:
        cat = SkillCategory(name=cat_name, slug=cat_slug, icon=cat_icon, display_order=cat_order)
        db.add(cat)
        db.flush()
        for idx, (s_name, s_prof, s_level, s_feat, s_color) in enumerate(skills_list, start=1):
            s = Skill(
                category_id=cat.id,
                name=s_name,
                proficiency_percentage=s_prof,
                level=s_level,
                is_featured=s_feat,
                badge_color=s_color,
                display_order=idx,
            )
            db.add(s)

    # 5. Professional Work Experience
    # Innefu Labs
    exp1 = WorkExperience(
        company_name="Innefu Labs",
        parent_group=None,
        designation="Senior Software Engineer",
        employment_type="Full-time",
        location="New Delhi, India",
        start_date="Jan'26",
        end_date="Present",
        is_current=True,
        tech_stack_summary="Python, FastAPI, Django, Flask, LangGraph, Model Context Protocol (MCP), Neo4j, Elasticsearch, RAG, Microservices",
        display_order=1,
    )
    db.add(exp1)
    db.flush()

    exp1_bullets = [
        ("Designing and developing high-performance backend systems using Python, Django, FastAPI, and Flask microservices for internal tooling and AI-agent utility endpoints, following clean, Microservices architecture principles.", "Architecture", 1),
        ("Building RESTful and Asynchronous APIs using FastAPI (async/await) and Django for secure, scalable, low-latency services; maintaining ETL pipelines for structured and semi-structured data ingestion.", "Async APIs", 2),
        ("Implementing graph-based data modeling using Neo4j and tuning Elasticsearch indexing/Full-Text Search for high-speed analytics and search-driven features, backed by System Design principles.", "Graph & Search", 3),
        ("Designing and developing autonomous AI Agents using LangGraph to coordinate multi-agent teams, managing state transitions, persistent chat memory, and self-correction loops.", "Agentic AI", 4),
        ("Architecting custom Model Context Protocol (MCP) servers to securely connect LLM agents to local data stores, graph databases, and external tool endpoints.", "MCP Servers", 5),
        ("Implementing Retrieval-Augmented Generation (RAG) using Vector Embeddings and Semantic Search for AI-powered knowledge retrieval, and integrating LangChain orchestration for prompt-based automation workflows.", "GenAI & RAG", 6),
        ("Contributing to core product architecture involving scalable backend systems, Graph Databases (Neo4j), and search-driven architectures (Elasticsearch) for high-performance, intelligent querying.", "Scalable Design", 7),
    ]
    for bullet, tag, b_order in exp1_bullets:
        db.add(ExperienceHighlight(experience_id=exp1.id, bullet_point=bullet, highlight_tag=tag, display_order=b_order))

    # Shyam Future Tech
    exp2 = WorkExperience(
        company_name="Shyam Future Tech Pvt. Ltd.",
        parent_group="Group of Shyam Steel",
        designation="Back-end Developer",
        employment_type="Full-time",
        location="Kolkata, India",
        start_date="May'22",
        end_date="Dec'25",
        is_current=False,
        tech_stack_summary="Django, DRF, FastAPI, Flask, SQLAlchemy, Celery, Redis, Kafka, Zookeeper, AWS, Docker, Kubernetes, PySpark, Elasticsearch, OpenCV",
        display_order=2,
    )
    db.add(exp2)
    db.flush()

    exp2_bullets = [
        ("Designed, developed, and maintained scalable RESTful APIs using Django, DRF, FastAPI, and Flask — including standalone Flask microservices for internal automation utilities and third-party integrations — following Microservices and Event-Driven Architecture principles.", "Microservices", 1),
        ("Built FastAPI and Flask services with SQLAlchemy for ORM-based database management, schema migrations, and Async APIs using async/await, dependency injection, and connection pooling.", "FastAPI & ORM", 2),
        ("Optimized backend performance using Django ORM, SQLAlchemy, middleware, serializers, query optimization, indexing, and profiling techniques.", "Performance", 3),
        ("Integrated Redis for caching, rate limiting, and session management, and Celery for distributed task queues and scheduled/background jobs.", "Caching & Queues", 4),
        ("Built and maintained Apache Kafka (cloud-managed & self-hosted) with Zookeeper for real-time data streaming and distributed event processing.", "Event Streaming", 5),
        ("Implemented AWS services (Lambda, SNS, SQS, EC2, S3, RDS, ECS, ECR, CloudWatch) for serverless processing, messaging, monitoring, and scalable infrastructure.", "AWS Cloud", 6),
        ("Implemented Elasticsearch for high-performance indexing and Full-Text Search; managed large datasets using MySQL, PostgreSQL, and MongoDB with schema/query optimization.", "Databases & Search", 7),
        ("Containerized applications using Docker and deployed Microservices on Kubernetes, managing deployments, configs, secrets, and rolling updates.", "Docker & K8s", 8),
        ("Used PySpark and Spark SQL for distributed processing of large datasets (100GB+) across multi-node clusters integrated with Kafka, S3, and relational databases.", "Big Data", 9),
        ("Integrated Machine Learning and Computer Vision pipelines using TensorFlow, OpenCV, DeepFace, Pandas, and NumPy for intelligent automation and predictive processing.", "Computer Vision", 10),
        ("Boosted API performance and scalability via ORM query optimization, Redis caching, and Asynchronous FastAPI services, achieving 99.9% uptime on a Cloud-Native AWS architecture (EC2, Lambda, SQS, SNS, Docker, Kubernetes).", "High Availability", 11),
    ]
    for bullet, tag, b_order in exp2_bullets:
        db.add(ExperienceHighlight(experience_id=exp2.id, bullet_point=bullet, highlight_tag=tag, display_order=b_order))

    # NS Matrix Services (Associate Technical Project Manager)
    exp3 = WorkExperience(
        company_name="NS Matrix Services Pvt. Ltd.",
        parent_group=None,
        designation="Associate Technical Project Manager",
        employment_type="Full-time",
        location="New Delhi, India",
        start_date="Sept'17",
        end_date="Dec'17",
        is_current=False,
        tech_stack_summary="Django, Flask, REST APIs, ORM Optimization, Redis, Celery, AWS, Docker",
        display_order=3,
    )
    db.add(exp3)
    db.flush()

    exp3_bullets = [
        ("Designed and developed scalable Django & Flask REST APIs, architecting modular back-end services using OOP principles, design patterns, and clean architecture.", "Clean Architecture", 1),
        ("Implemented advanced Django ORM and database optimizations (indexing, joins, annotations, prefetch/select_related, stored procedures) to support high-volume transactional workloads.", "ORM Optimization", 2),
        ("Integrated Redis caching and Celery-based Asynchronous tasks to improve API performance and automate background workflows; deployed applications on AWS (EC2, RDS, S3) with CI/CD pipelines and Docker containers.", "Async & Deployment", 3),
    ]
    for bullet, tag, b_order in exp3_bullets:
        db.add(ExperienceHighlight(experience_id=exp3.id, bullet_point=bullet, highlight_tag=tag, display_order=b_order))

    # NS Matrix Services (Technical Trainee)
    exp4 = WorkExperience(
        company_name="NS Matrix Services Pvt. Ltd.",
        parent_group=None,
        designation="Technical Trainee",
        employment_type="Internship",
        location="New Delhi, India",
        start_date="June'17",
        end_date="Sept'17",
        is_current=False,
        tech_stack_summary="Python, Django, Flask, MVC/MVT Architecture, SQLite, Query Optimization",
        display_order=4,
    )
    db.add(exp4)
    db.flush()

    exp4_bullets = [
        ("Assisted in developing Django and Flask-based REST APIs, learning modular backend design using OOP principles and MVC/MVT architecture; gained hands-on experience with Django ORM and query optimization.", "Backend Trainee", 1),
    ]
    for bullet, tag, b_order in exp4_bullets:
        db.add(ExperienceHighlight(experience_id=exp4.id, bullet_point=bullet, highlight_tag=tag, display_order=b_order))

    # 6. Architectural Case Studies & Projects
    projects = [
        Project(
            title="Autonomous Multi-Agent Orchestrator",
            tagline="Stateful Agentic Workflows with LangGraph, Persistent Memory & Self-Correction",
            category="Agentic AI",
            architecture_summary=(
                "Architected a collaborative multi-agent swarm using LangGraph to automate complex, multi-step analytical and "
                "engineering workflows. Configured state transition graphs, checkpointed memory in PostgreSQL/Redis, and implemented "
                "self-correcting reflection loops to validate LLM outputs before dispatching to client microservices."
            ),
            key_features=(
                "LangGraph stateful workflow coordination\n"
                "Dynamic agent supervisor routing requests to specialized worker agents\n"
                "Persistent short-term & long-term conversation memory\n"
                "Automated validation & retry loops for structured JSON responses\n"
                "FastAPI async endpoint layer for streaming agent tokens"
            ),
            tech_stack="Python, FastAPI, LangGraph, LangChain, Redis, PostgreSQL, OpenAI / Hugging Face",
            github_url="https://github.com/vivekjaiswal/langgraph-multi-agent-orchestrator",
            badge="Agentic AI",
            icon="bot",
            featured=True,
            display_order=1,
        ),
        Project(
            title="Custom Model Context Protocol (MCP) Server",
            tagline="Standardized Secure Tool Execution & Context Interface for Enterprise LLMs",
            category="Agentic AI",
            architecture_summary=(
                "Engineered a high-performance Model Context Protocol (MCP) server that securely bridges frontier LLMs with internal "
                "data sources, Neo4j knowledge graphs, and relational databases. Implemented granular permission scopes, token-efficient "
                "payload filtering, and async tool invocation handlers."
            ),
            key_features=(
                "Compliant with Anthropic / open Model Context Protocol (MCP) specification\n"
                "Read & write tool bindings for Neo4j Cypher queries and SQL databases\n"
                "Strict schema validation via Pydantic v2\n"
                "FastAPI SSE (Server-Sent Events) and JSON-RPC 2.0 communication transports\n"
                "Zero-trust authentication and audit logging for all LLM actions"
            ),
            tech_stack="Python, FastAPI, MCP SDK, Neo4j, SQLAlchemy, Docker",
            github_url="https://github.com/vivekjaiswal/mcp-enterprise-server",
            badge="Enterprise MCP",
            icon="cpu",
            featured=True,
            display_order=2,
        ),
        Project(
            title="Event-Driven Real-Time Data Streaming Platform",
            tagline="Distributed High-Throughput Event Processing Engine Handling 100GB+ Data",
            category="Distributed Systems",
            architecture_summary=(
                "Built an enterprise event-driven architecture utilizing Apache Kafka, Zookeeper, Celery, and PySpark for large-scale "
                "distributed data ingestion and analytical processing. Supported high-concurrency event ingestion with exactly-once "
                "semantics, Redis caching, and resilient failover."
            ),
            key_features=(
                "Apache Kafka cluster management with partitioned consumer groups\n"
                "PySpark batch and micro-batch ETL pipelines across multi-node clusters\n"
                "Redis-backed sliding window rate limiter and hot-key cache\n"
                "Celery distributed workers for CPU-bound background transformations\n"
                "Achieved 99.9% availability across AWS cloud infrastructure"
            ),
            tech_stack="Python, Apache Kafka, PySpark, Redis, Celery, AWS (EC2, S3, SQS), Docker",
            github_url="https://github.com/vivekjaiswal/kafka-spark-streaming-pipeline",
            badge="Big Data & Kafka",
            icon="zap",
            featured=True,
            display_order=3,
        ),
        Project(
            title="Hybrid Knowledge Graph & Semantic Search Engine",
            tagline="Graph-Powered Entity Navigation with Neo4j and Elasticsearch Dense Retrieval",
            category="Search & Vector",
            architecture_summary=(
                "Developed a dual-engine search system marrying Neo4j's relational graph traversal with Elasticsearch full-text and "
                "dense vector embeddings. Provided sub-100ms semantic search, entity disambiguation, and context-augmented query expansion "
                "for enterprise intelligence portals."
            ),
            key_features=(
                "Hybrid search combining BM25 keyword matching with dense vector cosine similarity\n"
                "Neo4j Cypher graph queries for deep multi-hop relationship exploration\n"
                "Automated data synchronization pipeline between relational DB and Elasticsearch\n"
                "Asynchronous FastAPI gateway with connection pooling and response compression"
            ),
            tech_stack="Python, FastAPI, Neo4j, Elasticsearch, FAISS, Pytest, Docker",
            github_url="https://github.com/vivekjaiswal/graph-semantic-search-engine",
            badge="Graph & Search",
            icon="search",
            featured=True,
            display_order=4,
        ),
    ]
    db.add_all(projects)

    # 7. Education & Certifications
    edu = Education(
        degree="Bachelor of Technology (B.Tech.)",
        field_of_study="Computer Science and Engineering",
        institution="GLA University",
        location="Mathura (U.P.), India",
        completion_year="2017",
        grade="CGPA: 7.61",
    )
    db.add(edu)

    achievements = [
        Achievement(
            title="HackerRank 5-Star Certifications (Python & SQL)",
            badge="HackerRank 5-Star",
            description="Earned top 5-star rating in both Python programming and SQL database querying, demonstrating deep foundational algorithmic problem-solving and relational data management proficiency.",
            category="Certifications",
            icon="award",
            display_order=1,
        ),
        Achievement(
            title="Scalable Microservices Architecture",
            badge="System Architecture",
            description="Designed and implemented modular Microservices-based back-end architecture capable of supporting high-traffic enterprise applications with independent service deployment, horizontal scalability, and fault isolation.",
            category="System Design",
            icon="layers",
            display_order=2,
        ),
        Achievement(
            title="Generative AI & Agentic LLM Pipelines",
            badge="AI Innovation",
            description="Built and integrated production AI applications leveraging Hugging Face Transformers, NLP pipelines, Prompt Engineering, LangChain, and LangGraph multi-agent LLM workflows for document understanding and conversational capabilities.",
            category="Generative AI",
            icon="bot",
            display_order=3,
        ),
        Achievement(
            title="Enterprise MCP & RAG Infrastructure",
            badge="Advanced AI",
            description="Designed scalable AI-enabled backend systems supporting Semantic Search, intelligent automation, custom Model Context Protocol (MCP) servers, and Retrieval-Augmented Generation (RAG) with Vector Databases.",
            category="AI Engineering",
            icon="cpu",
            display_order=4,
        ),
        Achievement(
            title="Dual Expertise: Backend & Machine Learning",
            badge="Full Lifecycle",
            description="Combined strong Backend Engineering with Machine Learning proficiency, integrating ML models into production-ready Django/FastAPI applications to enhance predictive functionality and user experience.",
            category="Engineering",
            icon="code",
            display_order=5,
        ),
        Achievement(
            title="High-Impact Technical Leadership",
            badge="Impact & Reliability",
            description="Progressed to managing high-impact and complex projects across enterprise domains, reflecting consistent trust in technical expertise, architecture rigor, and delivery reliability.",
            category="Leadership",
            icon="trending-up",
            display_order=6,
        ),
    ]
    db.add_all(achievements)

    # 8. Soft Skills
    soft_skills = [
        SoftSkill(name="Analytical Problem-Solving", description="Deconstructing complex distributed system bottlenecks with algorithmic precision", icon="check", display_order=1),
        SoftSkill(name="Systematic Thinking", description="Designing end-to-end architectures considering latency, fault tolerance, and data consistency", icon="check", display_order=2),
        SoftSkill(name="Technical Communication", description="Articulating architectural decisions clearly to cross-functional teams and stakeholders", icon="check", display_order=3),
        SoftSkill(name="Proactive Initiative", description="Driving modern technology adoption including Agentic AI, MCP, and event streaming", icon="check", display_order=4),
        SoftSkill(name="Mentorship & Knowledge Sharing", description="Fostering engineering excellence, code reviews, and TDD practices", icon="check", display_order=5),
        SoftSkill(name="Stakeholder Collaboration", description="Aligning engineering roadmaps with business KPIs and uptime requirements", icon="check", display_order=6),
    ]
    db.add_all(soft_skills)

    db.commit()
