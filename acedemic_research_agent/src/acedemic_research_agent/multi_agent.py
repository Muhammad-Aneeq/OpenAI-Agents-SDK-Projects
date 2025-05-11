from agents import Agent, set_tracing_disabled
from agents.model_settings import ModelSettings
from agent_tools.search_tool import serper_search
from models.acedemic_models import (
    LiteratureSearchPlan,
    AnalysisSummary,
    ResearchReportData,
    VerificationResult
)
from prompts.acedemic_prompts import (
    PLANNER_AGENT_INSTRUCTIONS,
    SEARCH_AGENT_INSTRUCTIONS,
    METHODOLOGY_AGENT_INSTRUCTIONS,
    THEORY_AGENT_INSTRUCTIONS,
    WRITER_AGENT_INSTRUCTIONS,
    VERIFIER_AGENT_INSTRUCTIONS
)

set_tracing_disabled(True)

planner_agent: Agent = Agent(
    name="AcademicPlannerAgent",
    instructions=PLANNER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=LiteratureSearchPlan,
)

search_agent: Agent = Agent(
    name="AcademicSearchAgent",
    instructions=SEARCH_AGENT_INSTRUCTIONS,
    tools=[serper_search],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

methodology_agent: Agent = Agent(
    name="MethodologyAnalystAgent",
    instructions=METHODOLOGY_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=AnalysisSummary,
)

theory_agent: Agent = Agent(
    name="TheoryAnalystAgent",
    instructions=THEORY_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=AnalysisSummary,
)

writer_agent: Agent = Agent(
    name="AcademicWriterAgent",
    instructions=WRITER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ResearchReportData,
)

verifier_agent: Agent = Agent(
    name="AcademicVerifierAgent",
    instructions=VERIFIER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=VerificationResult,
)