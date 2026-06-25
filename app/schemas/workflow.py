from pydantic import BaseModel, Field


class CandidateScreenRequest(BaseModel):
    candidate_text: str = Field(min_length=1)
    job_description: str = Field(min_length=1)


class CandidateScreenResponse(BaseModel):
    normalized_input: str
    fit_summary: str
    recommendation: str

