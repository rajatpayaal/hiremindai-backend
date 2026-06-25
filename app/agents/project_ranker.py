from typing import Any


class ProjectRankerAgent:
    name = "project_ranker"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        projects = payload.get("projects", []) or []
        ranked_projects = [
            {"rank": index + 1, "project": project, "reason": "Pending semantic ranking"}
            for index, project in enumerate(projects)
        ]
        return {"ranked_projects": ranked_projects}

