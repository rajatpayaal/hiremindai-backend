from fastapi import APIRouter, Depends

from app.agents.registry import get_agent
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicPayload, PublicResponse
from app.services.public_store import create_record

projects_router = APIRouter()
planner_router = APIRouter()
writer_router = APIRouter()
ats_router = APIRouter()
grammar_router = APIRouter()
hallucination_router = APIRouter()
recruiter_router = APIRouter()
self_reflection_router = APIRouter()
rewrite_router = APIRouter()
validation_router = APIRouter()
cover_letter_router = APIRouter()
email_router = APIRouter()
interview_router = APIRouter()


# ─── Projects ────────────────────────────────────────────────────────────────

@projects_router.post("/rank", response_model=PublicResponse)
async def rank_projects(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Rank resume projects by relevance to a job description.

    Expected payload keys: `projects` (list), `job_description`.
    """
    return PublicResponse(data=await get_agent("project_ranker").run(payload.payload))


# ─── Planner ─────────────────────────────────────────────────────────────────

@planner_router.post("/resume", response_model=PublicResponse)
async def plan_resume(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Generate a structured resume writing plan based on a parsed resume and job description.

    Expected payload keys: `parsed_resume`, `job_description`, `target_role` (optional),
    `company_name` (optional).
    """
    parsed_resume = payload.payload.get("parsed_resume", {})
    job_description = payload.payload.get("job_description", "")
    target_role = payload.payload.get("target_role", "")
    company_name = payload.payload.get("company_name", "")

    # Use skill matcher for gap analysis
    match_result = await get_agent("skill_matcher").run(
        {"resume_text": str(parsed_resume), "job_description": job_description}
    )

    plan = {
        "target_role": target_role,
        "company_name": company_name,
        "skill_gap_analysis": match_result,
        "sections_to_include": [
            "summary",
            "experience",
            "skills",
            "projects",
            "education",
            "certifications",
        ],
        "writing_strategy": {
            "tone": "professional",
            "emphasis": "quantifiable achievements",
            "ats_keywords": match_result.get("matched_skills", []),
            "missing_keywords": match_result.get("missing_skills", []),
        },
        "recommendations": [
            f"Highlight {skill} in your experience bullets."
            for skill in match_result.get("missing_skills", [])[:5]
        ],
    }
    record = create_record("history", {"type": "plan", "plan": plan, "owner_id": current_user.id})
    return PublicResponse(id=record["id"], data={"plan": plan})


# ─── Writer ───────────────────────────────────────────────────────────────────

@writer_router.post("/resume", response_model=PublicResponse)
async def write_resume(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Generate an optimized resume draft using the Resume Writer agent.

    Expected payload keys: `parsed_resume`, `job_description`, `plan` (optional),
    `candidate_name`, `target_role`.
    """
    result = await get_agent("resume_writer").run(payload.payload)
    record = create_record("history", {"type": "draft", "draft": result, "owner_id": current_user.id})
    return PublicResponse(id=record["id"], data=result)


# ─── ATS ──────────────────────────────────────────────────────────────────────

@ats_router.post("/optimize", response_model=PublicResponse)
async def optimize_ats(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Optimize a resume draft for ATS (Applicant Tracking Systems).

    Expected payload keys: `resume_draft`, `job_description`.
    """
    return PublicResponse(data=await get_agent("ats_optimizer").run(payload.payload))


@ats_router.post("/score", response_model=PublicResponse)
async def score_ats(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Score a resume against a job description for ATS compatibility (0–100).

    Expected payload keys: `resume_text`, `job_description`.
    """
    return PublicResponse(data=await get_agent("ats_scorer").run(payload.payload))


# ─── Grammar ─────────────────────────────────────────────────────────────────

@grammar_router.post("/check", response_model=PublicResponse)
async def check_grammar(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Check grammar, spelling, and style of a resume or cover letter.

    Expected payload key: `text`.
    """
    return PublicResponse(data=await get_agent("grammar_checker").run(payload.payload))


# ─── Hallucination ───────────────────────────────────────────────────────────

@hallucination_router.post("/check", response_model=PublicResponse)
async def check_hallucination(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Detect fabricated or hallucinated content in an AI-generated resume.

    Expected payload keys: `original_resume`, `generated_resume`.
    """
    return PublicResponse(data=await get_agent("hallucination_guard").run(payload.payload))


# ─── Recruiter Review ────────────────────────────────────────────────────────

@recruiter_router.post("/review", response_model=PublicResponse)
async def recruiter_review(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Simulate a recruiter's review of a resume for a given role.

    Expected payload keys: `resume_text`, `job_description`.
    """
    return PublicResponse(data=await get_agent("reviewer").run(payload.payload))


# ─── Self Reflection ─────────────────────────────────────────────────────────

@self_reflection_router.post("", response_model=PublicResponse)
async def self_reflection(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Run a self-reflection pass over a resume draft to identify improvements.

    Expected payload keys: `resume_draft`, `job_description`, `previous_scores` (optional).
    """
    return PublicResponse(data=await get_agent("self_reflection").run(payload.payload))


# ─── Rewrite ─────────────────────────────────────────────────────────────────

@rewrite_router.post("", response_model=PublicResponse)
async def rewrite(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Rewrite a resume draft incorporating feedback from previous review passes.

    Expected payload keys: `resume_draft`, `job_description`,
    `recruiter_feedback` (optional), `self_reflection_feedback` (optional).
    """
    writer_payload = payload.payload.get("writer_payload", payload.payload)
    result = await get_agent("resume_writer").run(writer_payload)
    return PublicResponse(data=result)


# ─── Validation ──────────────────────────────────────────────────────────────

@validation_router.post("/final", response_model=PublicResponse)
async def final_validation(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Run a final validation pass over a completed resume (hallucination + grammar + ATS).

    Expected payload keys: `resume_text`, `job_description`, `original_resume`.
    """
    return PublicResponse(data=await get_agent("final_validator").run(payload.payload))


# ─── Cover Letter ─────────────────────────────────────────────────────────────

@cover_letter_router.post("/generate", response_model=PublicResponse)
async def generate_cover_letter(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Generate a personalised cover letter using the Cover Letter agent.

    Expected payload keys: `resume_text`, `job_description`,
    `candidate_name`, `company_name`, `target_role`.
    """
    return PublicResponse(data=await get_agent("cover_letter").run(payload.payload))


# ─── Recruiter Email ─────────────────────────────────────────────────────────

@email_router.post("/generate", response_model=PublicResponse)
async def generate_email(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Generate a cold-outreach recruiter email.

    Expected payload keys: `candidate_name`, `target_role`, `company_name`,
    `resume_summary`, `job_description`.
    """
    return PublicResponse(data=await get_agent("recruiter_email").run(payload.payload))


# ─── Interview ───────────────────────────────────────────────────────────────

@interview_router.post("/generate", response_model=PublicResponse)
async def generate_interview(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Generate tailored interview questions for a candidate+role combination.

    Expected payload keys: `resume_text`, `job_description`, `target_role`,
    `num_questions` (optional, default 10).
    """
    return PublicResponse(data=await get_agent("interview_generator").run(payload.payload))
