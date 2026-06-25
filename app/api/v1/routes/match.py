from fastapi import APIRouter, Depends

from app.agents.registry import get_agent
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicPayload, PublicResponse

router = APIRouter()


@router.post("/skills", response_model=PublicResponse)
async def match_skills(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Match resume skills against a job description using the Skill Matcher agent.

    Expected payload keys: `resume_text`, `job_description`.
    """
    result = await get_agent("skill_matcher").run(payload.payload)
    return PublicResponse(data=result)


@router.post("/experience", response_model=PublicResponse)
async def match_experience(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Match candidate experience against job requirements.

    Expected payload keys: `resume_text`, `job_description`.
    Returns an experience-match breakdown and a weighted score.
    """
    # Reuse skill matcher with experience-focused context
    raw = await get_agent("skill_matcher").run(
        {**payload.payload, "mode": "experience"}
    )
    return PublicResponse(
        data={
            "experience_match": raw,
            "score": raw.get("score", 0.0),
        }
    )


@router.post("/overall", response_model=PublicResponse)
async def match_overall(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Compute an overall candidate-to-job match score (skills + experience).

    Expected payload keys: `resume_text`, `job_description`.
    """
    skill_result = await get_agent("skill_matcher").run(payload.payload)
    exp_result = await get_agent("skill_matcher").run(
        {**payload.payload, "mode": "experience"}
    )
    overall_score = (skill_result.get("score", 0.0) + exp_result.get("score", 0.0)) / 2
    return PublicResponse(
        data={
            "skills": skill_result,
            "experience": exp_result,
            "overall_score": round(overall_score, 4),
        }
    )
