from app.agents.ats_optimizer import ATSOptimizerAgent
from app.agents.ats_scorer import ATSScorerAgent
from app.agents.company_intelligence import CompanyIntelligenceAgent
from app.agents.cover_letter import CoverLetterAgent
from app.agents.final_validator import FinalValidatorAgent
from app.agents.grammar_checker import GrammarCheckerAgent
from app.agents.hallucination_guard import HallucinationGuardAgent
from app.agents.interview_generator import InterviewGeneratorAgent
from app.agents.jd_parser import JDParserAgent
from app.agents.project_ranker import ProjectRankerAgent
from app.agents.recruiter_email import RecruiterEmailAgent
from app.agents.resume_parser import ResumeParserAgent
from app.agents.resume_writer import ResumeWriterAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.self_reflection import SelfReflectionAgent
from app.agents.skill_matcher import SkillMatcherAgent
from app.agents.base import Agent

AGENTS: dict[str, Agent] = {
    ResumeParserAgent.name: ResumeParserAgent(),
    JDParserAgent.name: JDParserAgent(),
    CompanyIntelligenceAgent.name: CompanyIntelligenceAgent(),
    SkillMatcherAgent.name: SkillMatcherAgent(),
    ProjectRankerAgent.name: ProjectRankerAgent(),
    ResumeWriterAgent.name: ResumeWriterAgent(),
    ATSOptimizerAgent.name: ATSOptimizerAgent(),
    GrammarCheckerAgent.name: GrammarCheckerAgent(),
    HallucinationGuardAgent.name: HallucinationGuardAgent(),
    ReviewerAgent.name: ReviewerAgent(),
    ATSScorerAgent.name: ATSScorerAgent(),
    SelfReflectionAgent.name: SelfReflectionAgent(),
    FinalValidatorAgent.name: FinalValidatorAgent(),
    CoverLetterAgent.name: CoverLetterAgent(),
    RecruiterEmailAgent.name: RecruiterEmailAgent(),
    InterviewGeneratorAgent.name: InterviewGeneratorAgent(),
}


def get_agent(name: str) -> Agent:
    return AGENTS[name]
