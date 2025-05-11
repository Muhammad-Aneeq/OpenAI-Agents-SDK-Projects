import random
from agents import (
    Agent,
    handoff,
    RunContextWrapper,
    set_tracing_disabled,
    set_default_openai_client,
    set_default_openai_api
    )
from models.airline_models import AirlineAgentContext
from prompts.airline_prompts import (
    FAQ_AGENT_INSTRUCTIONS,
    SEAT_BOOKING_AGENT_INSTRUCTIONS,
    TRIAGE_AGENT_INSTRUCTIONS
)
from agent_tools.faq_tool import faq_lookup_tool
from agent_tools.update_seat_tool import update_seat
from agents.model_settings import ModelSettings
from openai import AsyncOpenAI

from dotenv import load_dotenv
import os

_:bool = load_dotenv()
# GEMINI_API_KEY =  os.getenv("API_KEY")
# BASE_URL =  os.getenv("BASE_URL")


### HOOKS
set_tracing_disabled(True)
# set_default_openai_api("chat_completions")

# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url=BASE_URL,
# )

# set_default_openai_client(external_client)

async def on_seat_booking_handoff(context: RunContextWrapper[AirlineAgentContext]) -> None:
    flight_number = f"FLT-{random.randint(100, 999)}"
    context.context.flight_number = flight_number


### AGENTS

faq_agent: Agent = Agent[AirlineAgentContext](
    name= "FAQ Agent",
    handoff_description="A helpful agent that can answer questions about the airline.",
    instructions=FAQ_AGENT_INSTRUCTIONS,
    tools=[faq_lookup_tool],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

seat_booking_agent: Agent = Agent[AirlineAgentContext](
    name="Seat Booking Agent",
    handoff_description="A helpful agent that can update a seat on a flight.",
    instructions=SEAT_BOOKING_AGENT_INSTRUCTIONS,
    tools=[update_seat],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

triage_agent: Agent = Agent[AirlineAgentContext](
    name="Triage Agent",
    handoff_description="A triage agent that can delegate a customer's request to the appropriate agent.",
    instructions=TRIAGE_AGENT_INSTRUCTIONS,
    handoffs=[
        faq_agent,
        handoff(agent=seat_booking_agent, on_handoff=on_seat_booking_handoff)
    ],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini"
)

faq_agent.handoffs.append(triage_agent)
seat_booking_agent.handoffs.append(triage_agent)
