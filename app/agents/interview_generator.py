from typing import Any


class InterviewGeneratorAgent:
    name = "interview_generator"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        skills = payload.get("skills", []) or []
        questions = [f"Describe a project where you used {skill}." for skill in skills]
        return {"questions": questions}

