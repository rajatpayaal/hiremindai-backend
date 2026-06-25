from typing import Any


class CompanyIntelligenceAgent:
    name = "company_intelligence"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        company_name = str(payload.get("company_name", "")).strip()
        return {
            "company_name": company_name,
            "industry": "",
            "hiring_signals": [],
            "culture_signals": [],
            "notes": "",
        }

