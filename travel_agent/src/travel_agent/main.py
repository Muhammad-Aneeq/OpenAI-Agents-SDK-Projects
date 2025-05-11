import chainlit as cl
from travel_agent.agents_flow import config, create_travel_plan

# Ordered list of keys for travel details
QUESTIONS = ["origin", "city", "travel_dates", "interests"]

# Mapping each key to its corresponding improved question prompt
QUESTION_PROMPTS = {
    "origin": "Could you please share your starting point (origin) for your trip?",
    "city": "What destination city would you like to explore?",
    "travel_dates": "When are you planning to travel? (Please provide the travel dates or month)",
    "interests": "What are your primary travel interests? (e.g., Cultural Tours, Photography)"
}

@cl.on_chat_start
async def start():
    # Initialize session variables: an empty dict for travel details and a question index
    cl.user_session.set("travel_details", {})
    cl.user_session.set("question_index", 0)
    # Ask the first question using an improved prompt
    first_question = QUESTION_PROMPTS[QUESTIONS[0]]
    await cl.Message(content=f"Hi, welcome to the Travel Bot! {first_question}").send()

@cl.on_message
async def main(message):
    # Retrieve current session data
    travel_details = cl.user_session.get("travel_details") or {}
    question_index = cl.user_session.get("question_index") or 0

    # Save the answer for the current question
    if question_index < len(QUESTIONS):
        key = QUESTIONS[question_index]
        travel_details[key] = message.content
        cl.user_session.set("travel_details", travel_details)
        
        # Move to the next question
        question_index += 1
        cl.user_session.set("question_index", question_index)
        
        if question_index < len(QUESTIONS):
            next_key = QUESTIONS[question_index]
            next_question = QUESTION_PROMPTS[next_key]
            await cl.Message(content=next_question).send()
        else:
            # All questions answered; first, show a summary of the collected details
   
            # Send a loading message while generating the travel plan
            loading_msg = cl.Message(content="Thanks for providing your details. Generating your travel plan, please wait... ⏳")
            await loading_msg.send()
            
            # Call the create_travel_plan function with the collected details.
            result = create_travel_plan(travel_details,config)
            
            # Construct the final message using the result returned by your agent.
            itinerary = result.get("itinerary", "No itinerary provided.")
            city = result.get("city", "No city info provided.")
            local_insights = result.get("local_insights", "No local insights available.")
            
            final_output = (
                f"Your travel plan is ready!\n\n"
                f"**Itinerary:** {itinerary}"
            )
            # Set the new content
            loading_msg.content = final_output

            # Update the loading message with the final output
            await loading_msg.update()
    else:
        # Handle the case where all questions have already been answered
        await cl.Message(content="You have already provided all the required details.").send()
