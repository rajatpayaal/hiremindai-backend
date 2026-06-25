from typing import Any

from pydantic import BaseModel, Field


class CandidateScreenRequest(BaseModel):
    candidate_text: str = Field(min_length=1)
    job_description: str = Field(min_length=1)


class CandidateScreenResponse(BaseModel):
    normalized_input: str
    fit_summary: str
    recommendation: str


class ResumeOptimizationRequest(BaseModel):
    resume_text: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    company_name: str | None = None
    candidate_name: str | None = None
    target_role: str | None = None
    max_rewrites: int = Field(default=1, ge=0, le=3)


class ResumeOptimizationResponse(BaseModel):
    final_resume: str
    cover_letter: str
    recruiter_email: dict[str, Any]
    interview_questions: list[str]
    ats_score: float
    needs_rewrite: bool
    validation: dict[str, Any]
    steps: dict[str, Any]
