# Travel Planning Assistant

This project provides an AI-powered Travel Planning Assistant that uses a multi-agent workflow to assist users in planning their trips. The system asks users for details about their trip, such as origin, destination city, travel dates, and interests. Based on this input, it generates a personalized travel plan, suggesting the best city, providing local insights, and creating a detailed 7-day itinerary

### Code Flow Overview

1. **Initialization**:
   - The system begins by asking users a series of questions related to their trip, such as origin, destination city, travel dates, and travel interests.
   - The user’s responses are stored in session variables.

2. **Agents**:
   - **CitySelectionExpert**: Verifies the user's selected destination city based on factors like travel convenience, cultural richness, and affordability. It may suggest an alternative city if needed.
   - **LocalTourGuide**: Provides detailed local insights for the selected city, including attractions, cultural customs, and hidden gems. It tailors its suggestions to the user's travel interests (e.g., cultural tours, photography).
   - **TravelAgent**: Creates a 7-day travel itinerary based on the confirmed city, local insights, and the user’s interests. It includes daily plans, budget estimates, packing suggestions, and safety tips.

3. **Workflow**:
   - **User Input**: The user provides details about their trip, such as origin, destination, travel dates, and interests.
   - **City Selection**: The `CitySelectionExpert` validates or adjusts the user’s destination choice.
   - **Local Insights**: The `LocalTourGuide` provides in-depth local information about the selected city, focusing on the user’s interests.
   - **Itinerary Creation**: The `TravelAgent` generates a detailed travel itinerary, incorporating local insights and ensuring that it aligns with the user’s preferences.
   - **Final Output**: The assistant provides a comprehensive travel plan, including the itinerary, city information, and local insights.

4. **Interactive Interface**:
   - The system uses **Streamlit** to provide a user-friendly interface for trip planning. Users can select their destination, input travel details, and receive a personalized travel plan.

---

### Getting Started

Follow these steps to set up and run the Travel Planning Assistant locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py
