from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.workflow import (
    CandidateScreenRequest,
    CandidateScreenResponse,
    ResumeOptimizationRequest,
    ResumeOptimizationResponse,
)
from app.services.public_store import create_record
from app.services.workflows import optimize_resume, screen_candidate

router = APIRouter()


@router.post("/candidate-screening", response_model=CandidateScreenResponse)
async def candidate_screening(
    payload: CandidateScreenRequest,
    current_user: User = Depends(get_current_user),
) -> CandidateScreenResponse:
    """
    End-to-end candidate screening workflow.

    Parses both the candidate resume and the job description, then generates
    a fit-summary with a hire/no-hire recommendation.
    """
    result = await screen_candidate(payload)
    # Persist to history
    create_record(
        "history",
        {"type": "candidate_screening", "result": result.model_dump(), "owner_id": current_user.id},
    )
    return result


@router.post("/resume-optimization", response_model=ResumeOptimizationResponse)
async def resume_optimization(
    payload: ResumeOptimizationRequest,
    current_user: User = Depends(get_current_user),
) -> ResumeOptimizationResponse:
    """
    End-to-end resume optimisation workflow.

    Runs the full multi-agent pipeline: parse → plan → write → ATS score →
    grammar check → hallucination guard → recruiter review → self-reflection →
    optional rewrite → final validation → cover letter → recruiter email →
    interview questions.
    """
    result = await optimize_resume(payload)
    # Persist to history
    create_record(
        "history",
        {
            "type": "resume_optimization",
            "result": result.model_dump(),
            "owner_id": current_user.id,
        },
    )
    return result
