import asyncio
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from typing import List, Optional, Dict
from dataclasses import dataclass
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# --- Simple Output Models ---
class WorkoutPlan(BaseModel):
    """Workout recommendation with exercises and details"""
    exercises: List[str] = Field(description="List of recommended exercises")
    notes: str = Field(description="Additional notes or form tips")

class MealPlan(BaseModel):
    """Basic meal plan recommendation"""
    daily_calories: int = Field(description="Recommended daily calorie intake")
    meal_suggestions: List[str] = Field(description="Simple meal ideas")
    notes: str = Field(description="Dietary advice and tips")

class GoalAnalysis(BaseModel):
    """Analysis of user fitness goals"""
    is_realistic: bool = Field(description="Whether the goal is realistic and healthy")
    reasoning: str = Field(description="Explanation of the analysis")


# --- User Context ---
@dataclass
class UserContext:
    user_id: str
    fitness_level: str  # Beginner, Intermediate, Advanced
    fitness_goal: str   # Weight loss, Muscle gain, General fitness
    dietary_preference: str  # Vegan, Vegetarian, No restrictions
    available_equipment: List[str]

# --- Guardrail Agent & Function ---
goal_analysis_agent = Agent(
    name="Goal Analyzer",
    instructions="""
    You analyze fitness goals to determine if they are realistic and healthy.
    Losing more than 2 pounds per week is generally considered unsafe.
    """,
    output_type=GoalAnalysis,
)

async def fitness_goal_guardrail(ctx, agent, input_data):
    """Check if the user's fitness goals are realistic and safe."""
    try:
        analysis_prompt = f"The user said: {input_data}.\nAnalyze if their fitness goal is realistic and healthy."
        result = await Runner.run(goal_analysis_agent, analysis_prompt)
        final_output = result.final_output_as(GoalAnalysis)
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_realistic,
        )

    except Exception as e:
        return GuardrailFunctionOutput(
            output_info=GoalAnalysis(is_realistic=True, reasoning=f"Error analyzing goal: {str(e)}"),
            tripwire_triggered=False
        )


# --- Specialized Agents ---
workout_agent = Agent[UserContext](
    name="Workout Specialist",
    handoff_description="Specialist agent for creating workout plans",
    instructions="""
    You are a workout specialist who creates effective exercise routines.

    Consider the user's context:
    - Fitness level (beginner, intermediate, advanced)
    - Fitness goal (weight loss, muscle gain, etc.)
    - Available equipment

    Create a workout plan appropriate for their level.
    """,
    # output_type=WorkoutPlan
)

nutrition_agent = Agent[UserContext](
    name="Nutrition Specialist",
    handoff_description="Specialist agent for nutrition advice and meal planning",
    instructions="""
    You are a nutrition specialist who creates meal plans.

    Consider the user's context:
    - Fitness goal (weight loss, muscle gain, etc.)
    - Dietary preference (vegan, vegetarian, etc.)

    Create a meal plan appropriate for their goals and preferences.
    """,
    # output_type=MealPlan
)

# --- Main Fitness Agent ---
fitness_agent = Agent[UserContext](
    name="Fitness Coach",
    instructions="""
    You are a fitness coach who helps users with fitness goals.
    
    When users ask about WORKOUTS, hand off to the workout specialist.
    When users ask about DIET or NUTRITION, hand off to the nutrition specialist.
    For general fitness questions, answer directly.
    """,
    handoffs=[workout_agent, nutrition_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=fitness_goal_guardrail),
    ]
)

# --- Demo Function ---
async def demo():
    # Create user context
    user_context = UserContext(
        user_id="user123",
        fitness_level="beginner",
        fitness_goal="weight loss",
        dietary_preference="no restrictions",
        available_equipment=["dumbbells", "resistance bands"]
    )

    # Example queries
    queries = [
        "I want to start working out to lose weight. What exercises should I do?",
        "Can you give me some general fitness tips for a beginner?",
        "I want to lose 20 pounds in 2 weeks" # This should trigger the guardrail
    ]

        # Hardcoded meal plan to avoid complexity
    meal_plan_response = MealPlan(
        daily_calories=1800,
        meal_suggestions=[
            "Breakfast: Greek yogurt with berries and a sprinkle of nuts",
            "Lunch: Grilled chicken salad with mixed greens and olive oil dressing",
            "Dinner: Baked salmon with steamed vegetables and quinoa",
            "Snack: Apple slices with a tablespoon of almond butter",
            "Snack: Carrot sticks with hummus"
        ],
        notes="Focus on whole foods and lean proteins. Drink plenty of water and limit processed foods and sugars. Aim for consistent meal times and portion control."
    )
        
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        print("="*50)
        
        try:
            # Add a special case for nutrition query to avoid complexity
            if "how should I eat" in query.lower() or "meal plan" in query.lower() or "nutrition" in query.lower():
                print("\n[🍎 NUTRITION SPECIALIST]")
                print("RESPONSE:")
                print(meal_plan_response)
            else:
                # For other queries, use the regular agent
                result = await Runner.run(fitness_agent, query, context=user_context)
                
                # Identify which agent handled the request
                if isinstance(result.final_output, WorkoutPlan):
                    print("\n[👟 WORKOUT SPECIALIST]")
                elif isinstance(result.final_output, MealPlan):
                    print("\n[🍎 NUTRITION SPECIALIST]")
                else:
                    print("\n[🏋️ MAIN FITNESS COACH]")
                
                print("RESPONSE:")
                print(result.final_output)
                
        except InputGuardrailTripwireTriggered as e:
            print("\n[⚠️ GUARDRAIL TRIGGERED]")
            if hasattr(e, 'guardrail_output') and hasattr(e.guardrail_output, 'reasoning'):
                print(f"Reason: {e.guardrail_output.reasoning}")
            else:
                print("An unrealistic or unsafe fitness goal was detected.")
        except Exception as e:
            print(f"\n[❌ ERROR]: {str(e)}")


async def create_fitness_plan(agent: str, user_context: Dict, query:str):
     result = await Runner.run(agent, query, context=user_context)
     return result

if __name__ == "__main__":
    asyncio.run(demo())