from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.llm import get_gemini_chat
from app.prompts.candidate_screening import CANDIDATE_SCREENING_PROMPT


class CandidateScreeningState(TypedDict):
    candidate_text: str
    job_description: str
    normalized_input: str
    fit_summary: str
    recommendation: str


def normalize_input(state: CandidateScreeningState) -> CandidateScreeningState:
    candidate = " ".join(state["candidate_text"].split())
    job = " ".join(state["job_description"].split())
    return {
        **state,
        "normalized_input": f"Candidate: {candidate}\n\nJob: {job}",
    }


async def analyze_fit(state: CandidateScreeningState) -> CandidateScreeningState:
    if not state["normalized_input"]:
        return {**state, "fit_summary": "No input was available for analysis."}

    llm = get_gemini_chat()
    prompt = (
        f"{CANDIDATE_SCREENING_PROMPT}\n\n"
        f"{state['normalized_input']}"
    )
    response = await llm.ainvoke(prompt)
    return {**state, "fit_summary": str(response.content)}


def generate_recommendation(state: CandidateScreeningState) -> CandidateScreeningState:
    summary = state["fit_summary"].lower()
    if "strong" in summary or "excellent" in summary:
        recommendation = "shortlist"
    elif "risk" in summary or "missing" in summary:
        recommendation = "review_manually"
    else:
        recommendation = "hold"

    return {**state, "recommendation": recommendation}


def build_candidate_screening_workflow():
    workflow = StateGraph(CandidateScreeningState)
    workflow.add_node("normalize_input", normalize_input)
    workflow.add_node("analyze_fit", analyze_fit)
    workflow.add_node("generate_recommendation", generate_recommendation)

    workflow.set_entry_point("normalize_input")
    workflow.add_edge("normalize_input", "analyze_fit")
    workflow.add_edge("analyze_fit", "generate_recommendation")
    workflow.add_edge("generate_recommendation", END)

    return workflow.compile()


candidate_screening_workflow = build_candidate_screening_workflow()


async def run_candidate_screening_workflow(
    candidate_text: str,
    job_description: str,
) -> CandidateScreeningState:
    initial_state: CandidateScreeningState = {
        "candidate_text": candidate_text,
        "job_description": job_description,
        "normalized_input": "",
        "fit_summary": "",
        "recommendation": "",
    }
    return await candidate_screening_workflow.ainvoke(initial_state)
