from typing import Any


class ResumeParserAgent:
    name = "resume_parser"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        resume_text = str(payload.get("resume_text", "")).strip()
        skills = [
            skill.strip()
            for skill in resume_text.replace("\n", ",").split(",")
            if skill.strip() and len(skill.strip()) <= 40
        ][:20]
        return {
            "raw_text": resume_text,
            "sections": {
                "summary": "",
                "experience": [],
                "education": [],
                "skills": skills,
                "projects": [],
            },
        }
