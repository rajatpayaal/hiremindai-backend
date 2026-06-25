from typing import Any

from pydantic import BaseModel, Field


class PublicPayload(BaseModel):
    """Generic payload wrapper for agent/action endpoints."""
    payload: dict[str, Any] = Field(default_factory=dict)


class PublicResponse(BaseModel):
    """Standard API response envelope."""
    id: str | None = None
    status: str = "success"
    data: dict[str, Any] = Field(default_factory=dict)


class TextPayload(BaseModel):
    """Simple text payload for checker-style endpoints."""
    text: str = Field(default="", description="Text input for parser/checker style APIs.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class ResumeParsePayload(BaseModel):
    """Payload for /resume/parse — raw resume text."""
    resume_text: str = Field(min_length=1, description="Full plain-text content of the resume.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class JobParsePayload(BaseModel):
    """Payload for /job/parse — raw job description text."""
    job_description: str = Field(min_length=1, description="Full plain-text content of the job description.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class MatchPayload(BaseModel):
    """Payload for /match/* endpoints."""
    resume_text: str = Field(min_length=1, description="Candidate resume text.")
    job_description: str = Field(min_length=1, description="Target job description.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class CompanyAnalyzePayload(BaseModel):
    """Payload for /company/analyze."""
    company_name: str = Field(min_length=1, description="Name of the target company.")
    job_description: str = Field(default="", description="Optional job description for context.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class CoverLetterPayload(BaseModel):
    """Payload for /cover-letter/generate."""
    resume_text: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    candidate_name: str = Field(default="")
    company_name: str = Field(default="")
    target_role: str = Field(default="")
    tone: str = Field(default="professional", description="Writing tone: professional | friendly | enthusiastic")


class RecruiterEmailPayload(BaseModel):
    """Payload for /email/generate."""
    candidate_name: str = Field(min_length=1)
    target_role: str = Field(min_length=1)
    company_name: str = Field(default="")
    resume_summary: str = Field(default="")
    job_description: str = Field(default="")


class InterviewPayload(BaseModel):
    """Payload for /interview/generate."""
    resume_text: str = Field(min_length=1)
    job_description: str = Field(min_length=1)
    target_role: str = Field(default="")
    num_questions: int = Field(default=10, ge=1, le=50)
