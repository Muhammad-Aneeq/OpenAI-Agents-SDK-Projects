# Financial Research Assistant

This project provides an AI-powered Financial Research Assistant designed to help researchers and analysts conduct comprehensive financial assessments. The system supports planning, searching for financial data, performing financial analysis, writing reports, and verifying the final report. It utilizes specialized agents for different tasks in the workflow.

### Code Flow Overview

1. **Initialization**:
   - The `FinancialResearchManager` orchestrates the entire research process, including planning, searching, analysis, writing, and verification.
   - The workflow involves the following steps:
     - **Planning**: The `FinancialPlannerAgent` generates a search plan based on the user's query.
     - **Searching**: The `FinancialSearchAgent` performs financial searches based on the search plan.
     - **Analysis**: The `FundamentalsAnalystAgent` and `RiskAnalystAgent` perform financial analysis on the gathered data.
     - **Writing**: The `FinancialWriterAgent` drafts a comprehensive financial report.
     - **Verification**: The `VerificationAgent` ensures the quality and correctness of the final report.

2. **Agents**:
   - **FinancialPlannerAgent**: Creates a plan for searching financial data based on the input query.
   - **FinancialSearchAgent**: Performs financial searches for the specified query and collects relevant data.
   - **FundamentalsAnalystAgent**: Analyzes financial data and provides insights into key financial metrics.
   - **RiskAnalystAgent**: Assesses financial risks and identifies potential red flags.
   - **FinancialWriterAgent**: Writes a detailed financial report, including an executive summary, analysis, and recommendations.
   - **VerificationAgent**: Verifies the financial report and assesses its validity.

3. **Workflow**:
   - **Search Plan**: The `FinancialResearchManager` creates a search plan based on the user’s query.
   - **Performing Searches**: The system then performs searches based on the plan and retrieves relevant data.
   - **Analysis**: The system analyzes the data using specialized tools (fundamentals and risk analysis).
   - **Report Writing**: Once the analysis is complete, the system drafts a comprehensive report.
   - **Verification**: The report undergoes verification to ensure its quality and accuracy.

4. **Interactive Interface**:
   - The system uses **Chainlit** to handle the interaction with the user. It receives queries, processes them, and presents the results.

---

### Getting Started

Follow these steps to set up and run the Financial Research Assistant locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py
