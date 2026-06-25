from typing import Any


class ATSScorerAgent:
    name = "ats_scorer"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        matched_skills = payload.get("matched_skills", []) or []
        missing_skills = payload.get("missing_skills", []) or []
        total = len(matched_skills) + len(missing_skills)
        score = round((len(matched_skills) / total) * 100, 2) if total else 0.0
        return {
            "ats_score": score,
            "passed": score >= 70,
            "notes": "Score is based on matched required skills in the current scaffold.",
        }

