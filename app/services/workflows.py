from app.schemas.workflow import (
    CandidateScreenRequest,
    CandidateScreenResponse,
    ResumeOptimizationRequest,
    ResumeOptimizationResponse,
)
from app.workflows.candidate_screening import run_candidate_screening_workflow
from app.workflows.resume_optimization import run_resume_optimization_workflow


async def screen_candidate(payload: CandidateScreenRequest) -> CandidateScreenResponse:
    result = await run_candidate_screening_workflow(
        candidate_text=payload.candidate_text,
        job_description=payload.job_description,
    )
    return CandidateScreenResponse(**result)


async def optimize_resume(payload: ResumeOptimizationRequest) -> ResumeOptimizationResponse:
    result = await run_resume_optimization_workflow(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
        company_name=payload.company_name or "",
        candidate_name=payload.candidate_name or "",
        target_role=payload.target_role or "",
        max_rewrites=payload.max_rewrites,
    )
    return ResumeOptimizationResponse(**result)
