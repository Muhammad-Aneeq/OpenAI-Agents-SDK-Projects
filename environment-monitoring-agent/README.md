# Environmental Monitoring and Sustainability Assessment System

This project provides an AI-powered system for environmental monitoring and sustainability assessment. It helps assess the environmental status of a given location by collecting data, analyzing it, and generating a comprehensive report. The system allows users to specify a location and, optionally, a primary environmental concern (e.g., deforestation, pollution) to focus the assessment.

### Code Flow Overview

1. **Initialization**:
   - The system starts with the `EnvironmentalMonitorManager`, which orchestrates the environmental assessment process. 
   - The process involves multiple steps: creating a site profile, developing a monitoring plan, collecting environmental data, analyzing the data, and finally generating a report.

2. **Agents**:
   - **EnvironmentalPlanningAgent**: Develops an environmental monitoring plan based on the location and any specified concerns.
   - **EnvironmentalDataAgent**: Collects environmental data related to the monitoring plan, such as air quality, water quality, and biodiversity.
   - **EnvironmentalAnalystAgent**: Analyzes the collected data and integrates it with the site profile and monitoring plan to provide insights into environmental conditions.
   - **EnvironmentalReportAgent**: Generates a comprehensive environmental report, including an executive summary, environmental status assessment, and recommendations.

3. **Workflow**:
   - **Site Profile**: The system starts by creating a profile of the site based on basic environmental information about the location.
   - **Monitoring Plan**: The system generates a tailored environmental monitoring plan based on the site profile and any primary environmental concerns.
   - **Data Collection**: The system collects environmental data, such as air and water quality, using the monitoring plan.
   - **Data Analysis**: The system analyzes the collected data, integrating it with the site profile and monitoring plan to generate insights.
   - **Report Generation**: Finally, the system generates a detailed environmental report, summarizing the findings, environmental status, and recommendations.

4. **Interactive Interface**:
   - The system uses Streamlit to provide an interactive interface where users can input a location and specify a primary environmental concern. Once the user starts the assessment, the system handles the entire workflow and presents the results.

---

### Getting Started

Follow these steps to set up and run the Environmental Monitoring System locally:

```bash
# 1. Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

# 2. Install Dependencies
uv pip install -r pyproject.toml

# 3. Run the Application
uv run chainlit run main.py
