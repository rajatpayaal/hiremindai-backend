from typing import Any


class ATSOptimizerAgent:
    name = "ats_optimizer"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        missing_keywords = payload.get("missing_keywords", []) or []
        return {
            "ats_score": 0.0,
            "missing_keywords": missing_keywords,
            "recommendations": [
                f"Add measurable evidence for keyword: {keyword}" for keyword in missing_keywords
            ],
        }

