# Academic Research Assistant

This repository contains an AI-powered Academic Research Assistant designed to assist with research tasks such as literature search, report writing, methodology analysis, and verification. It orchestrates a full academic research workflow using multiple specialized agents. 

### Code Flow Overview

1. **Initialization**:
   - The `AcademicResearchManager` orchestrates the entire research workflow.
   - Upon starting the application, it initializes various agents for planning, searching, analyzing, writing, and verifying academic content.

2. **Agents**:
   - **AcademicPlannerAgent**: Plans the literature search strategy based on the input query.
   - **AcademicSearchAgent**: Performs the literature search based on the plan created by the `AcademicPlannerAgent`.
   - **MethodologyAnalystAgent**: Provides specialized analysis of research methodologies.
   - **TheoryAnalystAgent**: Analyzes theoretical frameworks relevant to the research topic.
   - **AcademicWriterAgent**: Writes the academic report based on the search results and analysis.
   - **AcademicVerifierAgent**: Verifies that the academic report adheres to high standards.

3. **Workflow**:
   - **Planning**: The `AcademicPlannerAgent` generates a literature search plan based on the research query.
   - **Searching**: The `AcademicSearchAgent` conducts the searches based on the plan.
   - **Writing**: The `AcademicWriterAgent`, along with tools like `MethodologyAnalystAgent` and `TheoryAnalystAgent`, writes a comprehensive academic report.
   - **Verification**: The `AcademicVerifierAgent` performs a peer review assessment to ensure the report meets academic standards.

---

### Getting Started

Follow the steps below to set up and run the project locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv 
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py