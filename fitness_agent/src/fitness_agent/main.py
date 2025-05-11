import chainlit as cl
from fitness_agent.agents_flow import fitness_agent, UserContext, WorkoutPlan, MealPlan, create_fitness_plan

# Ordered list of keys for fitness details
QUESTIONS = ["fitness_level", "fitness_goal", "dietary_preference", "available_equipment"]

# Mapping each key to its corresponding improved question prompt
QUESTION_PROMPTS = {
    "fitness_level": "What is your current fitness level? (Beginner, Intermediate, Advanced)",
    "fitness_goal": "What is your primary fitness goal? (e.g., Weight Loss, Muscle Gain, General Fitness)",
    "dietary_preference": "Do you have any dietary preferences or restrictions? (e.g., Vegan, Vegetarian, No Restrictions)",
    "available_equipment": "What fitness equipment do you have access to? (e.g., Dumbbells, Resistance Bands)"
}

# Function to start the fitness interaction and ask the first question
@cl.on_chat_start
async def start():
    # Initialize session variables: an empty dict for fitness details and a question index
    cl.user_session.set("fitness_details", {})
    cl.user_session.set("question_index", 0)
    # Ask the first question using the improved prompt
    first_question = QUESTION_PROMPTS[QUESTIONS[0]]
    await cl.Message(content=f""" # Fitness Assistant """).send()
    await cl.Message(content=f"Hi, welcome to the Fitness Coach! {first_question}").send()

# Function to process the user's responses and queries
@cl.on_message
async def main(message):
    # Retrieve current session data
    fitness_details = cl.user_session.get("fitness_details") or {}
    question_index = cl.user_session.get("question_index") or 0

    # If we are still asking questions to collect fitness details
    if question_index < len(QUESTIONS):
        # Save the current answer
        key = QUESTIONS[question_index]
        fitness_details[key] = message.content
        cl.user_session.set("fitness_details", fitness_details)
        
        # Move to the next question
        question_index += 1
        cl.user_session.set("question_index", question_index)
        
        # Ask the next question if there are any left
        if question_index < len(QUESTIONS):
            next_key = QUESTIONS[question_index]
            next_question = QUESTION_PROMPTS[next_key]
            await cl.Message(content=next_question).send()
        else:
            # Once all questions are answered, confirm and prompt for user queries
            await cl.Message(content="Thanks for providing your fitness details! Feel free to ask me any fitness-related queries.").send()
    else:
        # Process the user's fitness query after all details have been provided
        user_query = message.content  # This is the user's query after providing all details
        
        # Show loading message while processing the query
        loading_message = await cl.Message(content="Processing your query... Please wait.").send()

        # Create UserContext using the collected details
        user_context = UserContext(
            user_id="user123",  # This can be dynamic based on your app's user system
            fitness_level=fitness_details["fitness_level"],
            fitness_goal=fitness_details["fitness_goal"],
            dietary_preference=fitness_details["dietary_preference"],
            available_equipment=fitness_details["available_equipment"].split(", ")
        )

        try:
            # Run the fitness agent to handle the user's query
            result = await create_fitness_plan(fitness_agent, user_context, user_query)
            
            # Identify which part of the fitness agent responded (workout, meal plan, etc.)
            if isinstance(result.final_output, WorkoutPlan):
                response = f"[👟 WORKOUT PLAN] {result.final_output}"
            elif isinstance(result.final_output, MealPlan):
                response = f"[🍎 MEAL PLAN] {result.final_output}"
            else:
                response = f"[🏋️ FITNESS COACH] {result.final_output}"
            
            # Send the response to the user, replacing the loading message with the actual result
            await cl.Message(content=response).send()

        except Exception as e:
            # Handle any errors gracefully
            await cl.Message(content=f"An error occurred while processing your query: {str(e)}").send()
