from typing import Any


class ResumeWriterAgent:
    name = "resume_writer"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        profile = payload.get("profile", {}) or {}
        target_role = str(payload.get("target_role", "")).strip()
        matched_skills = payload.get("matched_skills", []) or []
        missing_skills = payload.get("missing_skills", []) or []
        ranked_projects = payload.get("ranked_projects", []) or []
        raw_text = str(profile.get("raw_text", "")).strip()
        project_lines = [
            f"- {item.get('project', item)}" if isinstance(item, dict) else f"- {item}"
            for item in ranked_projects[:3]
        ]
        skill_line = ", ".join(matched_skills or profile.get("skills", []))
        gap_line = ", ".join(missing_skills[:5])
        resume_text = "\n".join(
            line
            for line in [
                f"Target Role: {target_role}" if target_role else "",
                "Professional Summary",
                f"Candidate aligned to {target_role or 'the target role'} with relevant skills: {skill_line}.",
                "",
                "Core Skills",
                skill_line,
                "",
                "Relevant Projects",
                *project_lines,
                "",
                "Original Resume Context",
                raw_text,
                "",
                f"Keywords to strengthen: {gap_line}" if gap_line else "",
            ]
            if line is not None
        ).strip()
        return {
            "target_role": target_role,
            "resume_draft": resume_text,
        }
