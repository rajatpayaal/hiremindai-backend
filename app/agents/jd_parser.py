from typing import Any


class JDParserAgent:
    name = "jd_parser"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        jd_text = str(payload.get("job_description", "")).strip()
        return {
            "raw_text": jd_text,
            "role_title": "",
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "seniority": "",
        }

