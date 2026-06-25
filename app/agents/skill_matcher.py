from typing import Any


class SkillMatcherAgent:
    name = "skill_matcher"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        resume_skills = set(payload.get("resume_skills", []) or [])
        required_skills = set(payload.get("required_skills", []) or [])
        matched = sorted(resume_skills & required_skills)
        missing = sorted(required_skills - resume_skills)
        score = round(len(matched) / len(required_skills), 2) if required_skills else 0.0
        return {"matched_skills": matched, "missing_skills": missing, "score": score}

