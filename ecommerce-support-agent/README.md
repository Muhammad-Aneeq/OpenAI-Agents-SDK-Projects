# Ecommerce Support Assistant

This repository contains an AI-powered Ecommerce Support Assistant designed to help with various customer service tasks related to online shopping. The assistant can handle product information inquiries, order tracking, product returns, and customer queries. It uses specialized agents for each type of request and handles delegation through a triage agent.

### Code Flow Overview

1. **Initialization**:
   - The `main` function orchestrates the conversation by interacting with the triage agent. It tracks the conversation state and ensures that customer queries are directed to the appropriate agent.
   - The agents involved are:
     - **Product Information Agent**: Provides details about products.
     - **Order Tracking Agent**: Tracks orders and provides shipping updates.
     - **Returns Agent**: Handles product returns and refunds.
     - **Triage Agent**: Decides which specialized agent should handle a customer’s request based on their query.

2. **Agents**:
   - **Product Information Agent**: Answers queries about product details and specifications.
   - **Order Tracking Agent**: Provides order status, tracking information, and shipping updates.
   - **Returns Agent**: Handles product returns and refund requests.
   - **Triage Agent**: Evaluates customer queries and delegates them to the appropriate specialized agent.

3. **Workflow**:
   - **Triage Process**: The `Triage Agent` receives the customer’s message and evaluates whether it pertains to product information, order tracking, or returns.
   - **Product Information Handling**: If the query is related to products, the assistant invokes the **Product Information Agent** to provide the relevant details.
   - **Order Tracking Handling**: If the query involves order tracking, the assistant invokes the **Order Tracking Agent** to provide shipping updates.
   - **Returns Handling**: If the query involves product returns, the assistant invokes the **Returns Agent** to process the return and refund requests.
   - **Handoffs**: If needed, conversations can be handed off between agents. For example, if a product return request is identified, it’s handed off to the **Returns Agent**.

4. **Dynamic Progress Updates**:
   - As the system processes the request, it provides dynamic updates to the customer about the status of their query.

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
