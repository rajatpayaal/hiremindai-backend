from typing import Any


class ResumeParserAgent:
    name = "resume_parser"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        resume_text = str(payload.get("resume_text", "")).strip()
        return {
            "raw_text": resume_text,
            "sections": {
                "summary": "",
                "experience": [],
                "education": [],
                "skills": [],
                "projects": [],
            },
        }

