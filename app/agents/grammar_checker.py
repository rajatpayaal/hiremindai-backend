from typing import Any


class GrammarCheckerAgent:
    name = "grammar_checker"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        text = str(payload.get("text", "")).strip()
        return {"corrected_text": text, "issues": []}

