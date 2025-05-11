import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


city_selection_expert: Agent = Agent(
    name="CitySelectionExpert",
    instructions=(
        "Given a traveler’s origin, desired city, travel dates, and interests, confirm if the chosen city is ideal or suggest an alternative. "
        "Focus on factors like travel convenience, cultural richness, and affordability."
    )
)

local_tour_guide: Agent = Agent(
    name="LocalTourGuide",
    instructions=(
        "Provide detailed local insights, including attractions, cultural customs, and hidden gems. "
        "Focus particularly on opportunities for cultural tours and photography in the city."
    )
)

travel_agent: Agent = Agent(
    name="TravelAgent",
    instructions=(
        "Create a 7-day travel itinerary that includes detailed daily plans, budget estimates, packing suggestions, and safety tips. "
        "Incorporate local attractions and opportunities for cultural tours and photography."
    )
)


def create_travel_plan(user_input, run_config=None):
    # Extract input details
    origin = user_input.get("origin")
    desired_city = user_input.get("city")
    travel_dates = user_input.get("travel_dates")
    interests = user_input.get("interests")
    
    # Step 1: Confirm or adjust city selection using CitySelectionExpert
    city_response = Runner.run_sync(
        city_selection_expert,
        (
            f"User is traveling from {origin} to {desired_city} in {travel_dates}. "
            f"They are interested in {interests}. Should we proceed with {desired_city} or suggest a better option?"
        ),
        run_config=run_config
    )
    selected_city = city_response.final_output.strip()
    
    # Step 2: Get local insights from LocalTourGuide for the confirmed city
    insights_response = Runner.run_sync(
        local_tour_guide,
        (
            f"Provide detailed local insights for {selected_city}, "
            f"with a focus on {interests}."
        ),
        run_config=run_config
    )
    local_insights = insights_response.final_output.strip()
    
    # Step 3: Create the travel itinerary using TravelAgent, incorporating the local insights
    itinerary_response = Runner.run_sync(
        travel_agent,
        (
            f"Using the following local insights: {local_insights}, "
            f"create a 7-day travel itinerary for {selected_city} for travel dates {travel_dates}. "
            f"Ensure the itinerary reflects the user's interests in {interests}."
        ),
        run_config=run_config
    )
    
    return {
        "city": selected_city,
        "local_insights": local_insights,
        "itinerary": itinerary_response.final_output
    }


travel_details = {
    "origin": "New York, NY",
    "city": "Tokyo, Japan",
    "travel_dates": "April",
    "interests": "Cultural Tours, Photography"
}
# result = create_travel_plan(travel_details,config)

# print("result>>>",result)