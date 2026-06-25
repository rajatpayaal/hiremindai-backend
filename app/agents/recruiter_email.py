from typing import Any


class RecruiterEmailAgent:
    name = "recruiter_email"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        candidate_name = str(payload.get("candidate_name", "")).strip() or "Candidate"
        role_title = str(payload.get("role_title", "")).strip() or "the open role"
        company_name = str(payload.get("company_name", "")).strip() or "your team"
        return {
            "subject": f"Application for {role_title}",
            "body": (
                f"Hi,\n\n"
                f"I am reaching out to share my application for {role_title} at {company_name}. "
                f"My resume is attached for your review.\n\n"
                f"Best,\n{candidate_name}"
            ),
        }

