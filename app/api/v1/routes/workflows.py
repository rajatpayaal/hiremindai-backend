from fastapi import APIRouter

from app.schemas.workflow import CandidateScreenRequest, CandidateScreenResponse
from app.services.workflows import screen_candidate

router = APIRouter()


@router.post("/candidate-screening", response_model=CandidateScreenResponse)
async def candidate_screening(payload: CandidateScreenRequest) -> CandidateScreenResponse:
    return await screen_candidate(payload)
