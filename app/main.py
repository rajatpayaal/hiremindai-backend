from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

OPENAPI_TAGS = [
    {"name": "health", "description": "Service health checks. No authentication required."},
    {"name": "auth", "description": "User registration, login, JWT token issuance and refresh."},
    {"name": "files", "description": "Upload and manage files (PDF, DOCX, TXT)."},
    {"name": "resume", "description": "Store, retrieve, and AI-parse candidate resumes."},
    {"name": "job", "description": "Store, retrieve, and AI-parse job descriptions."},
    {"name": "company", "description": "Company intelligence analysis powered by AI."},
    {"name": "matching", "description": "Skill and experience matching between resume and JD."},
    {"name": "projects", "description": "AI-powered project ranking by job relevance."},
    {"name": "planner", "description": "Generate a structured resume writing plan."},
    {"name": "writer", "description": "AI resume writer — generates optimised resume drafts."},
    {"name": "ats", "description": "ATS optimisation and compatibility scoring."},
    {"name": "grammar", "description": "Grammar, spelling, and style checking."},
    {"name": "hallucination", "description": "Detect hallucinated/fabricated content in AI-generated resumes."},
    {"name": "recruiter", "description": "Simulated recruiter review of candidate resumes."},
    {"name": "self-reflection", "description": "Self-critique pass over resume drafts for iterative improvement."},
    {"name": "rewrite", "description": "Rewrite resume incorporating review feedback."},
    {"name": "validation", "description": "Final multi-agent validation of a completed resume."},
    {"name": "cover-letter", "description": "AI-generated personalised cover letters."},
    {"name": "email", "description": "AI-generated recruiter cold-outreach emails."},
    {"name": "interview", "description": "AI-generated tailored interview questions."},
    {"name": "workflows", "description": "End-to-end multi-agent pipelines (candidate screening, resume optimisation)."},
    {"name": "history", "description": "View and manage workflow run history."},
    {"name": "dashboard", "description": "User dashboard with aggregate statistics."},
    {"name": "users", "description": "Authenticated user profile management."},
    {"name": "agents", "description": "Developer mode — inspect and directly invoke individual AI agents."},
]


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        summary="HireMindAI Backend API",
        description=(
            "Complete REST API for AI-powered resume optimisation, candidate screening, "
            "ATS scoring, cover letter generation, and interview preparation. "
            "All endpoints (except `/api/v1/health`, `/api/v1/auth/register`, and `/api/v1/auth/login`) "
            "require a Bearer JWT in the `Authorization` header."
        ),
        version="0.1.0",
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=OPENAPI_TAGS,
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": True,
            "docExpansion": "list",
            "filter": True,
            "persistAuthorization": True,
        },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
