from typing import Any


class ReviewerAgent:
    name = "reviewer"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        artifact = str(payload.get("artifact", "")).strip()
        return {
            "artifact": artifact,
            "overall_score": 0.0,
            "strengths": [],
            "improvements": [],
        }

