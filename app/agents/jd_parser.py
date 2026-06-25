from typing import Any


class JDParserAgent:
    name = "jd_parser"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        jd_text = str(payload.get("job_description", "")).strip()
        keywords = [
            token.strip(".,:;()[]{}").strip()
            for token in jd_text.split()
            if len(token.strip(".,:;()[]{}")) > 2
        ]
        required_skills = list(dict.fromkeys(keywords[:20]))
        return {
            "raw_text": jd_text,
            "role_title": "",
            "required_skills": required_skills,
            "preferred_skills": [],
            "responsibilities": [],
            "seniority": "",
        }
