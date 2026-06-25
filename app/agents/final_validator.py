from typing import Any


class FinalValidatorAgent:
    name = "final_validator"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        resume = str(payload.get("resume", "")).strip()
        cover_letter = str(payload.get("cover_letter", "")).strip()
        interview_questions = payload.get("interview_questions", []) or []
        issues = []
        if not resume:
            issues.append("Resume is empty.")
        if not cover_letter:
            issues.append("Cover letter is empty.")
        if not interview_questions:
            issues.append("Interview questions are empty.")
        return {"is_valid": not issues, "issues": issues}

