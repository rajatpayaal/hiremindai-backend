from typing import Any


class CoverLetterAgent:
    name = "cover_letter"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        candidate_name = str(payload.get("candidate_name", "")).strip()
        company_name = str(payload.get("company_name", "")).strip()
        role_title = str(payload.get("role_title", "")).strip()
        return {
            "cover_letter": (
                f"Dear Hiring Team,\n\n"
                f"I am excited to apply for the {role_title} role at {company_name}.\n\n"
                f"Sincerely,\n{candidate_name}"
            ).strip()
        }

