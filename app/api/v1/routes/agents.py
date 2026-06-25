from fastapi import APIRouter, HTTPException, status

from app.agents.registry import AGENTS
from app.schemas.agents import AgentRunRequest, AgentRunResponse
from app.services.agents import run_agent

router = APIRouter()


@router.get("")
def list_agents() -> dict[str, list[str]]:
    return {"agents": sorted(AGENTS)}


@router.post("/{agent_name}/run", response_model=AgentRunResponse)
async def run_agent_by_name(agent_name: str, request: AgentRunRequest) -> AgentRunResponse:
    if agent_name not in AGENTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    return await run_agent(agent_name, request)

