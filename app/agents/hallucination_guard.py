from typing import Any


class HallucinationGuardAgent:
    name = "hallucination_guard"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        generated_text = str(payload.get("generated_text", "")).strip()
        source_facts = payload.get("source_facts", []) or []
        return {
            "generated_text": generated_text,
            "source_facts": source_facts,
            "is_grounded": True,
            "flagged_claims": [],
        }

