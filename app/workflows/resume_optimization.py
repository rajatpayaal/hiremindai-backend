from typing import Any, TypedDict

from app.agents.registry import get_agent


class ResumeOptimizationState(TypedDict):
    resume_text: str
    job_description: str
    company_name: str
    candidate_name: str
    target_role: str
    max_rewrites: int
    rewrite_count: int
    steps: dict[str, Any]
    final_resume: str
    cover_letter: str
    recruiter_email: dict[str, Any]
    interview_questions: list[str]
    ats_score: float
    needs_rewrite: bool
    validation: dict[str, Any]


async def run_resume_optimization_workflow(
    *,
    resume_text: str,
    job_description: str,
    company_name: str = "",
    candidate_name: str = "",
    target_role: str = "",
    max_rewrites: int = 1,
) -> ResumeOptimizationState:
    steps: dict[str, Any] = {}

    resume_parser = get_agent("resume_parser")
    jd_parser = get_agent("jd_parser")
    company_intelligence = get_agent("company_intelligence")
    skill_matcher = get_agent("skill_matcher")
    project_ranker = get_agent("project_ranker")
    resume_writer = get_agent("resume_writer")
    ats_optimizer = get_agent("ats_optimizer")
    grammar_checker = get_agent("grammar_checker")
    hallucination_guard = get_agent("hallucination_guard")
    reviewer = get_agent("reviewer")
    ats_scorer = get_agent("ats_scorer")
    self_reflection = get_agent("self_reflection")
    final_validator = get_agent("final_validator")
    cover_letter_agent = get_agent("cover_letter")
    recruiter_email_agent = get_agent("recruiter_email")
    interview_generator = get_agent("interview_generator")

    steps["resume_parser"] = await resume_parser.run({"resume_text": resume_text})
    resume_sections = steps["resume_parser"]["sections"]

    steps["jd_parser"] = await jd_parser.run({"job_description": job_description})
    jd = steps["jd_parser"]
    resolved_role = target_role or jd.get("role_title", "")

    steps["company_intelligence"] = await company_intelligence.run(
        {"company_name": company_name, "job_description": job_description}
    )

    steps["skill_experience_matching"] = await skill_matcher.run(
        {
            "resume_skills": resume_sections.get("skills", []),
            "required_skills": jd.get("required_skills", []),
            "resume_text": resume_text,
            "job_description": job_description,
        }
    )

    steps["project_ranker"] = await project_ranker.run(
        {
            "projects": resume_sections.get("projects", []),
            "job_description": job_description,
            "matched_skills": steps["skill_experience_matching"]["matched_skills"],
        }
    )

    steps["resume_planning"] = {
        "target_role": resolved_role,
        "focus_skills": steps["skill_experience_matching"]["matched_skills"],
        "keyword_gaps": steps["skill_experience_matching"]["missing_skills"],
        "top_projects": steps["project_ranker"]["ranked_projects"][:3],
    }

    rewrite_count = 0
    needs_rewrite = False
    final_resume = ""
    grammar_result: dict[str, Any] = {}
    guard_result: dict[str, Any] = {}
    review_result: dict[str, Any] = {}
    ats_result: dict[str, Any] = {"ats_score": 0.0, "passed": False}
    reflection_result: dict[str, Any] = {"needs_rewrite": False, "reasons": []}

    while True:
        writer_payload = {
            "profile": {
                "raw_text": resume_text,
                "skills": resume_sections.get("skills", []),
            },
            "target_role": resolved_role,
            "matched_skills": steps["skill_experience_matching"]["matched_skills"],
            "missing_skills": steps["skill_experience_matching"]["missing_skills"],
            "ranked_projects": steps["project_ranker"]["ranked_projects"],
            "rewrite_count": rewrite_count,
        }
        steps["resume_writer"] = await resume_writer.run(writer_payload)
        draft_resume = str(steps["resume_writer"]["resume_draft"])

        steps["ats_optimizer"] = await ats_optimizer.run(
            {"resume": draft_resume, "missing_keywords": steps["resume_planning"]["keyword_gaps"]}
        )
        optimized_resume = draft_resume

        grammar_result = await grammar_checker.run({"text": optimized_resume})
        steps["grammar_checker"] = grammar_result
        final_resume = str(grammar_result["corrected_text"])

        guard_result = await hallucination_guard.run(
            {"generated_text": final_resume, "source_facts": [resume_text, job_description]}
        )
        steps["hallucination_guard"] = guard_result

        review_result = await reviewer.run({"artifact": final_resume, "job_description": job_description})
        steps["recruiter_review"] = review_result

        ats_result = await ats_scorer.run(
            {
                "resume": final_resume,
                "matched_skills": steps["skill_experience_matching"]["matched_skills"],
                "missing_skills": steps["skill_experience_matching"]["missing_skills"],
            }
        )
        steps["ats_scoring"] = ats_result

        reflection_result = await self_reflection.run(
            {
                "ats_score": ats_result["ats_score"],
                "flagged_claims": guard_result["flagged_claims"],
                "review": review_result,
            }
        )
        steps["self_reflection"] = reflection_result
        needs_rewrite = bool(reflection_result["needs_rewrite"])

        if not needs_rewrite or rewrite_count >= max_rewrites:
            break
        rewrite_count += 1
        steps["rewrite"] = {
            "attempt": rewrite_count,
            "reasons": reflection_result["reasons"],
        }

    cover_letter_result = await cover_letter_agent.run(
        {
            "candidate_name": candidate_name,
            "company_name": company_name,
            "role_title": resolved_role,
            "resume": final_resume,
        }
    )
    steps["cover_letter"] = cover_letter_result

    recruiter_email_result = await recruiter_email_agent.run(
        {
            "candidate_name": candidate_name,
            "company_name": company_name,
            "role_title": resolved_role,
        }
    )
    steps["recruiter_email"] = recruiter_email_result

    interview_result = await interview_generator.run(
        {"skills": steps["skill_experience_matching"]["matched_skills"], "role_title": resolved_role}
    )
    steps["interview_generator"] = interview_result

    validation = await final_validator.run(
        {
            "resume": final_resume,
            "cover_letter": cover_letter_result["cover_letter"],
            "interview_questions": interview_result["questions"],
        }
    )
    steps["final_validation"] = validation

    return {
        "resume_text": resume_text,
        "job_description": job_description,
        "company_name": company_name,
        "candidate_name": candidate_name,
        "target_role": resolved_role,
        "max_rewrites": max_rewrites,
        "rewrite_count": rewrite_count,
        "steps": steps,
        "final_resume": final_resume,
        "cover_letter": cover_letter_result["cover_letter"],
        "recruiter_email": recruiter_email_result,
        "interview_questions": interview_result["questions"],
        "ats_score": float(ats_result["ats_score"]),
        "needs_rewrite": needs_rewrite,
        "validation": validation,
    }
