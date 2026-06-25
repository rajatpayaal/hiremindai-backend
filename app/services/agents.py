from app.agents.registry import get_agent
from app.schemas.agents import AgentRunRequest, AgentRunResponse


async def run_agent(agent_name: str, request: AgentRunRequest) -> AgentRunResponse:
    agent = get_agent(agent_name)
    result = await agent.run(request.payload)
    return AgentRunResponse(agent=agent_name, result=result)

