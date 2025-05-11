import asyncio
from models.content import ContentContext
from prompts.content_prompts import (
    CONTENT_MANAGER_INSTRUCTIONS,
    RESEARCH_SPECIALIST_INSTRUCTIONS,
    CONTENT_WRITER_INSTRUCTIONS,
    CONTENT_EDITOR_INSTRUCTIONS
)
from agents import Agent, Runner, handoff
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agent_tools.tools import research_topic

from agents.model_settings import ModelSettings
# Example of how to use the workflow with a single topic


 # Set up agents
content_manager = Agent(
        name="Content Manager",
        instructions=prompt_with_handoff_instructions(CONTENT_MANAGER_INSTRUCTIONS),
        model="gpt-4o-mini"
    )

research_specialist = Agent(
        name="Research Specialist",
        instructions=prompt_with_handoff_instructions(RESEARCH_SPECIALIST_INSTRUCTIONS),
        tools=[research_topic],
        model_settings=ModelSettings(tool_choice="required"),
        model="gpt-4o-mini"
    )

content_writer = Agent(
        name="Content Writer",
        instructions=prompt_with_handoff_instructions(CONTENT_WRITER_INSTRUCTIONS),
        model="gpt-4o-mini"
    )

content_editor = Agent(
        name="Content Editor",
        instructions=prompt_with_handoff_instructions(CONTENT_EDITOR_INSTRUCTIONS),
        model="gpt-4o-mini"
    )

content_editor = Agent(
        name="Content Editor",
        instructions=prompt_with_handoff_instructions(CONTENT_EDITOR_INSTRUCTIONS),
        model="gpt-4o-mini"
    )

    # Setting up handoffs between agents
content_manager.handoffs = [
        handoff(agent=research_specialist),
        handoff(agent=content_writer),
        handoff(agent=content_editor),
    ]
research_specialist.handoffs = [
        handoff(agent=content_manager)
    ]
content_writer.handoffs = [
        handoff(agent=content_manager)
    ]
content_editor.handoffs = [
        handoff(agent=content_manager)
    ]
