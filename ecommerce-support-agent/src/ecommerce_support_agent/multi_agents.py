import random
from agents import (
    Agent,
    handoff,
    RunContextWrapper,
    set_tracing_disabled,
    set_default_openai_api,
    set_default_openai_client
)
from openai import AsyncOpenAI
from models.ecommerce_models import EcommerceAgentContext
from prompts.ecommerce_prompts import (
    PRODUCT_INFO_AGENT_INSTRUCTIONS,
    ORDER_TRACKING_AGENT_INSTRUCTIONS,
    PRODUCT_RETURNS_AGENT_INSTRUCTIONS,
    TRIAGE_AGENT_INSTRUCTIONS
)
from agent_tools.product_lookup_tool import product_lookup_tool
from agent_tools.order_tracker_tool import track_order
from agent_tools.return_process_tool import process_return
from agents.model_settings import ModelSettings
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

async def on_returns_handoff(context: RunContextWrapper[EcommerceAgentContext]) -> None:
    # Perform any setup needed when handing off to returns agent
    if not context.context.customer_email:
        context.context.customer_email = f"customer{random.randint(1000, 9999)}@example.com"

product_info_agent: Agent = Agent[EcommerceAgentContext](
    name="Product Information Agent",
    handoff_description="An agent that provides detailed information about products.",
    instructions=PRODUCT_INFO_AGENT_INSTRUCTIONS,
    tools=[product_lookup_tool],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

order_tracking_agent = Agent[EcommerceAgentContext](
    name="Order Tracking Agent",
    handoff_description="An agent that can track orders and provide shipping updates.",
    instructions=ORDER_TRACKING_AGENT_INSTRUCTIONS,
    tools=[track_order],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

returns_agent = Agent[EcommerceAgentContext](
    name="Returns Agent",
    handoff_description="An agent that handles product returns and refunds.",
    instructions=PRODUCT_RETURNS_AGENT_INSTRUCTIONS,
    tools=[process_return],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

triage_agent = Agent[EcommerceAgentContext](
    name="Triage Agent",
    handoff_description="A triage agent that directs customer inquiries to specialized agents.",
    instructions=TRIAGE_AGENT_INSTRUCTIONS,
    handoffs=[
        product_info_agent,
        order_tracking_agent,
        handoff(agent=returns_agent, on_handoff=on_returns_handoff),
    ],
    # model="gemini-2.0-flash"
    model="gpt-4o-mini",
)

# Set up handoffs back to triage agent
product_info_agent.handoffs.append(triage_agent)
order_tracking_agent.handoffs.append(triage_agent)
returns_agent.handoffs.append(triage_agent)