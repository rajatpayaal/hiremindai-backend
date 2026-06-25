from app.schemas.workflow import CandidateScreenRequest, CandidateScreenResponse
from app.workflows.candidate_screening import run_candidate_screening_workflow


async def screen_candidate(payload: CandidateScreenRequest) -> CandidateScreenResponse:
    result = await run_candidate_screening_workflow(
        candidate_text=payload.candidate_text,
        job_description=payload.job_description,
    )
    return CandidateScreenResponse(**result)

