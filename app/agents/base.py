from typing import Any, Protocol


class Agent(Protocol):
    name: str

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        ...

