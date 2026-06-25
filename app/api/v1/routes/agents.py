from fastapi import APIRouter, Depends
from typing import Any

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.agents import AgentRunRequest, AgentRunResponse
from app.services.agents import run_agent

router = APIRouter()

AGENT_ALIASES: dict[str, str] = {
    "resume-parser": "resume_parser",
    "jd-parser": "jd_parser",
    "company-intelligence": "company_intelligence",
    "skill-matcher": "skill_matcher",
    "project-ranker": "project_ranker",
    "resume-writer": "resume_writer",
    "ats-optimizer": "ats_optimizer",
    "grammar-checker": "grammar_checker",
    "hallucination-guard": "hallucination_guard",
    "recruiter-review": "reviewer",
    "ats-scorer": "ats_scorer",
    "self-reflection": "self_reflection",
    "final-validator": "final_validator",
    "cover-letter": "cover_letter",
    "recruiter-email": "recruiter_email",
    "interview-generator": "interview_generator",
}


def _get_agent_description(internal_name: str) -> str:
    descriptions: dict[str, str] = {
        "resume_parser": "Parses raw resume text into structured sections (summary, experience, skills, projects, education).",
        "jd_parser": "Parses a job description into structured requirements, responsibilities, and keywords.",
        "company_intelligence": "Gathers and analyses intelligence about a target company from available context.",
        "skill_matcher": "Matches candidate skills against job requirements and returns a gap analysis with score.",
        "project_ranker": "Ranks resume projects by relevance to a target job description.",
        "resume_writer": "Writes or rewrites a resume optimised for a specific job description.",
        "ats_optimizer": "Optimises a resume draft to improve ATS pass-through rates.",
        "grammar_checker": "Checks grammar, spelling, and professional style of resume or cover letter text.",
        "hallucination_guard": "Detects fabricated or hallucinated content in AI-generated resume text.",
        "reviewer": "Simulates a senior recruiter's review of a resume for a given role.",
        "ats_scorer": "Scores a resume against a job description for ATS compatibility (0–100).",
        "self_reflection": "Runs a self-critique pass over a resume draft and suggests targeted improvements.",
        "final_validator": "Final validation pass combining hallucination guard + grammar + ATS scoring.",
        "cover_letter": "Generates a tailored cover letter for a candidate and role.",
        "recruiter_email": "Generates a professional cold-outreach email to a recruiter.",
        "interview_generator": "Generates targeted interview questions based on resume and job description.",
    }
    return descriptions.get(internal_name, "No description available.")


@router.get("", summary="List all available agents")
def list_agents(current_user: User = Depends(get_current_user)) -> dict[str, list[dict[str, str]]]:
    """List all available AI agents with their public alias and internal name."""
    agents_list = [
        {"alias": alias, "internal_name": internal}
        for alias, internal in sorted(AGENT_ALIASES.items())
    ]
    return {"agents": agents_list}


# Factory functions to generate unique endpoint handlers for FastAPI's OpenAPI generator
def create_run_endpoint(agent_alias: str, internal_name: str):
    async def run_endpoint(
        request: AgentRunRequest,
        current_user: User = Depends(get_current_user),
    ) -> AgentRunResponse:
        result = await run_agent(internal_name, request)
        return AgentRunResponse(agent=agent_alias, result=result.result)

    run_endpoint.__name__ = f"run_{agent_alias.replace('-', '_')}"
    run_endpoint.__doc__ = f"Run the {agent_alias} agent with input payload."
    return run_endpoint


def create_get_endpoint(agent_alias: str, internal_name: str):
    def get_endpoint(
        current_user: User = Depends(get_current_user),
    ) -> dict[str, str]:
        return {
            "alias": agent_alias,
            "internal_name": internal_name,
            "status": "available",
            "description": _get_agent_description(internal_name),
        }

    get_endpoint.__name__ = f"get_{agent_alias.replace('-', '_')}"
    get_endpoint.__doc__ = f"Get information and status of the {agent_alias} agent."
    return get_endpoint


# Register each agent's endpoints explicitly so they are fully displayed in Swagger UI
for alias, internal in AGENT_ALIASES.items():
    router.add_api_route(
        path=f"/{alias}",
        endpoint=create_get_endpoint(alias, internal),
        methods=["GET"],
        summary=f"Get {alias} metadata",
        response_model=dict[str, str],
        tags=[alias],
    )
    router.add_api_route(
        path=f"/{alias}/run",
        endpoint=create_run_endpoint(alias, internal),
        methods=["POST"],
        summary=f"Run {alias} agent",
        response_model=AgentRunResponse,
        tags=[alias],
    )
