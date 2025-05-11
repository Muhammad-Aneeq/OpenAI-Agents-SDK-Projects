# Fitness Coach Assistant

This project provides an AI-powered Fitness Coach Assistant designed to help users achieve their fitness goals by creating personalized workout and meal plans. The system asks users for details like their fitness level, fitness goal, dietary preferences, and available equipment. It then generates a fitness plan and provides responses based on the user's input, helping with both exercise routines and nutrition advice.

### Code Flow Overview

1. **Initialization**:
   - The system starts by asking users for basic fitness details through a series of questions, such as their fitness level, fitness goal, dietary preferences, and available equipment.
   - The user's responses are stored in session variables to be used in generating a personalized fitness plan.

2. **Agents**:
   - **Fitness Coach**: The main agent that coordinates the interaction. It delegates specific queries to specialized agents (Workout Specialist and Nutrition Specialist) based on user input.
   - **Workout Specialist**: Handles queries related to workout plans, including exercises and routines.
   - **Nutrition Specialist**: Handles queries related to meal planning and dietary advice.
   - **Goal Analyzer**: A special agent that checks if the user's fitness goals are realistic and healthy, ensuring that they do not involve unsafe practices like rapid weight loss.

3. **Workflow**:
   - **User Interaction**: The assistant collects fitness details from the user and then answers specific fitness-related queries.
   - **Delegation**: When a user asks about workouts, the system hands off the request to the **Workout Specialist**. If the query is about nutrition, it delegates to the **Nutrition Specialist**.
   - **Goal Verification**: Before proceeding with any plan, the system checks if the user's fitness goals are safe using the **Goal Analyzer** agent.
   - **Fitness Plan Creation**: Once all details are collected, the assistant generates a personalized workout and meal plan.

4. **Interactive Interface**:
   - The system uses **Chainlit** to manage communication between the user and the assistant. Users interact with the system by answering questions and asking queries, while the system provides tailored responses and recommendations.

---

### Getting Started

Follow the steps below to set up and run the Fitness Coach Assistant locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py
