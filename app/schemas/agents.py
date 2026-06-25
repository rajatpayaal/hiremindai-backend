from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    agent: str
    result: dict[str, Any]

