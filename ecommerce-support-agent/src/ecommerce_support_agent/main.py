import asyncio
from agents import (
    Agent,
    Runner,
    TResponseInputItem,
    MessageOutputItem,
    ItemHelpers,
    HandoffOutputItem,
    ToolCallItem,
    ToolCallOutputItem
)
from models.ecommerce_models import EcommerceAgentContext
from multi_agents import triage_agent
import chainlit as cl

conversation_active = False
input_items : list[TResponseInputItem] = []

async def main(query: str):
    global conversation_active  # Use this to track whether the conversation is active
    global input_items

    current_agent: Agent[EcommerceAgentContext] = triage_agent
    # input_items: list[TResponseInputItem] = []
    context = EcommerceAgentContext()

        # Append user input to the list
    input_items.append({"content": query, "role": "user"})

    result = await Runner.run(current_agent, input_items, context=context)

    # Process new items (responses from agent)
    new_messages = []
    for new_item in result.new_items:
        if isinstance(new_item, MessageOutputItem):
            message_content = ItemHelpers.text_message_output(new_item)
            new_messages.append(message_content)


     # Send all new messages only once
    if new_messages and not conversation_active:
        conversation_active = True
        for message in new_messages:
            await cl.Message(content=message).send()

    # After the messages are sent, reset the conversation_active flag
    conversation_active = False

    # Update input items for next cycle
    input_items = result.to_input_list()
    current_agent = result.last_agent



@cl.on_chat_start
async def on_chat_start():
    global conversation_active

    # Send a welcome message only once when the chat starts
    if not conversation_active:
        await cl.Message(content="""# Ecommerce Support Assistant
Welcome! I'm here to help with all your online shopping needs.
Ask me about products, order tracking, returns, shipping options, or any other questions about your shopping experience, and I'll provide friendly, helpful assistance.RetryClaude can make mistakes. Please double-check responses.""").send()



@cl.on_message
async def handle_query(message: str):
    global conversation_active

    """This function handles user input messages."""

    if message.content.strip():  # Ensure the message is not empty
        await main(message.content)  # Run the agent's response generation logic
    else:
        # If the user sends an empty message, you can prompt again or skip.
        await cl.Message(content="Please type something to continue.").send()

    # Reset conversation_active flag after sending a response
    conversation_active = False



# Start the Chainlit app
if __name__ == "__main__":
    cl.run(handle_query)
