from typing import Any


class ResumeWriterAgent:
    name = "resume_writer"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        profile = payload.get("profile", {}) or {}
        target_role = str(payload.get("target_role", "")).strip()
        return {
            "target_role": target_role,
            "resume_draft": {
                "headline": profile.get("headline", ""),
                "summary": "",
                "experience_bullets": [],
                "skills": profile.get("skills", []),
            },
        }

