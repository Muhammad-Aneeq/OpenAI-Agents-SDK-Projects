from models.financial_models import (
    AnalysisSummary,
    FinancialSearchPlan,
    VerificationResult,
    FinancialReportData
)
from prompts.financial_prompts import (
    ANALYST_AGENT_INSTRUCTIONS,
    PLANNER_AGENT_INSTRUCTIONS,
    RISK_ANALYST_AGENT_INSTRUCTIONS,
    SEARCH_AGENT_INSTRUCTIONS,
    VERIFIER_AGENT_INSTRUCTIONS,
    WRITER_AGENT_INSTRUCTIONS
)
from agent_tools.search_tool import serper_search
# from helper_functions.printer import Printer
from agents import Agent,set_tracing_disabled
from agents.model_settings import ModelSettings


set_tracing_disabled(True)

planner_agent: Agent = Agent(
    name="FinancialPlannerAgent",
    instructions=PLANNER_AGENT_INSTRUCTIONS,
    model="gpt-4o",
    output_type=FinancialSearchPlan,
)

search_agent: Agent = Agent(
    name="FinancialSearchAgent",
    instructions=SEARCH_AGENT_INSTRUCTIONS,
    tools=[serper_search],
    model_settings=ModelSettings(tool_choice="required"),
    model="gpt-4o",
)

financials_agent: Agent = Agent(
    name="FundamentalsAnalystAgent",
    instructions=ANALYST_AGENT_INSTRUCTIONS,
    output_type=AnalysisSummary,
    model="gpt-4o"
)

risk_agent: Agent = Agent(
    name="RiskAnalystAgent",
    instructions=RISK_ANALYST_AGENT_INSTRUCTIONS,
    output_type=AnalysisSummary,
    model="gpt-4o"
)

# Note: We will attach handoffs to specialist analyst agents at runtime in the manager.
# This shows how an agent can use handoffs to delegate to specialized subagents.
writer_agent: Agent = Agent(
    name="FinancialWriterAgent",
    instructions=WRITER_AGENT_INSTRUCTIONS,
    model="gpt-4o",
    output_type=FinancialReportData,
)

verifier_agent: Agent = Agent(
    name="VerificationAgent",
    instructions=VERIFIER_AGENT_INSTRUCTIONS,
    model="gpt-4o",
    output_type=VerificationResult,
)
