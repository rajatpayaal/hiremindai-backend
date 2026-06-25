from typing import Any


class SelfReflectionAgent:
    name = "self_reflection"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        ats_score = float(payload.get("ats_score", 0.0) or 0.0)
        flagged_claims = payload.get("flagged_claims", []) or []
        needs_rewrite = ats_score < 70 or bool(flagged_claims)
        reasons = []
        if ats_score < 70:
            reasons.append("ATS score is below threshold.")
        if flagged_claims:
            reasons.append("Generated content has ungrounded claims.")
        return {"needs_rewrite": needs_rewrite, "reasons": reasons}

