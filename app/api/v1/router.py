from fastapi import APIRouter

from app.api.v1.routes import (
    agents,
    auth,
    company,
    dashboard,
    files,
    health,
    history,
    job,
    match,
    public_actions,
    resume,
    users,
    workflows,
)

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(job.router, prefix="/job", tags=["job"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
api_router.include_router(match.router, prefix="/match", tags=["matching"])
api_router.include_router(public_actions.projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(public_actions.planner_router, prefix="/planner", tags=["planner"])
api_router.include_router(public_actions.writer_router, prefix="/writer", tags=["writer"])
api_router.include_router(public_actions.ats_router, prefix="/ats", tags=["ats"])
api_router.include_router(public_actions.grammar_router, prefix="/grammar", tags=["grammar"])
api_router.include_router(
    public_actions.hallucination_router,
    prefix="/hallucination",
    tags=["hallucination"],
)
api_router.include_router(public_actions.recruiter_router, prefix="/recruiter", tags=["recruiter"])
api_router.include_router(
    public_actions.self_reflection_router,
    prefix="/self-reflection",
    tags=["self-reflection"],
)
api_router.include_router(public_actions.rewrite_router, prefix="/rewrite", tags=["rewrite"])
api_router.include_router(public_actions.validation_router, prefix="/validation", tags=["validation"])
api_router.include_router(
    public_actions.cover_letter_router,
    prefix="/cover-letter",
    tags=["cover-letter"],
)
api_router.include_router(public_actions.email_router, prefix="/email", tags=["email"])
api_router.include_router(public_actions.interview_router, prefix="/interview", tags=["interview"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
