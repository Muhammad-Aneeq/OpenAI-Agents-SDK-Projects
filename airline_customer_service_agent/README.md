# Airline Customer Service Assistant

This repository contains an AI-powered Airline Customer Service Assistant designed to help with various customer service tasks, including flight bookings, answering frequently asked questions (FAQ), and triaging customer requests. It uses multiple specialized agents to handle different aspects of customer queries and requests.

### Code Flow Overview

1. **Initialization**:
   - The `main` function orchestrates the conversation by interacting with different agents, tracking the conversation state, and ensuring the appropriate agent handles the query.
   - The agents involved are:
     - **FAQ Agent**: Handles FAQs about the airline.
     - **Seat Booking Agent**: Manages seat booking and updates.
     - **Triage Agent**: Delegates the request to the appropriate agent based on the query.

2. **Agents**:
   - **FAQ Agent**: Answers general customer questions about the airline.
   - **Seat Booking Agent**: Handles seat bookings and updates on flights.
   - **Triage Agent**: Decides which agent should handle a particular request. It delegates the work to either the FAQ or Seat Booking agent based on the customer's query.

3. **Workflow**:
   - **Triage Process**: When a customer sends a message, the Triage Agent first evaluates the request and decides whether it should be handled by the FAQ Agent or Seat Booking Agent.
   - **FAQ Handling**: If the query is related to airline FAQs, the FAQ Agent processes it and returns a response.
   - **Seat Booking Handling**: If the query involves seat booking, the Seat Booking Agent updates the seat availability and returns relevant information.
   - **Handoffs**: If needed, agents can pass the conversation to another agent for further processing (e.g., from FAQ to Seat Booking or vice versa).

4. **Dynamic Progress Updates**:
   - The system updates the customer with progress messages as the agents process their requests, ensuring that they are informed throughout the entire interaction.

---

### Getting Started

Follow the steps below to set up and run the project locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py
