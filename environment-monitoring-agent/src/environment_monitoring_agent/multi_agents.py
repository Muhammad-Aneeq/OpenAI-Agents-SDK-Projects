from agents import Agent
from prompts.agent_prompts import (
    PLANNER_AGENT_INSTRUCTIONS,
    DATA_AGENT_INSTRUCTIONS,
    ANALYSIS_AGENT_INSTRUCTIONS,
    WRITER_AGENT_INSTRUCTIONS
)
from agent_tools.search_tool import serper_search
from dotenv import load_dotenv

_: bool = load_dotenv()

planner_agent: Agent = Agent(
    name="EnvironmentalPlanningAgent",
    instructions=PLANNER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
)

data_agent: Agent = Agent(
    name="EnvironmentalDataAgent",
    instructions=DATA_AGENT_INSTRUCTIONS,
    tools=[serper_search],
    model="gpt-4o-mini",
)

analysis_agent: Agent = Agent(
    name="EnvironmentalAnalystAgent",
    instructions=ANALYSIS_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
)

writer_agent: Agent = Agent(
    name="EnvironmentalReportAgent",
    instructions=WRITER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
)