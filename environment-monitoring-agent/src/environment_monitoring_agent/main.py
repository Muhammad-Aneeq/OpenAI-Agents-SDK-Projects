import asyncio
from rich.console import Console
from agents import (
    Runner
)
from typing import List
from multi_agents import (
    planner_agent,
    data_agent,
    analysis_agent,
    writer_agent
)
from helper_functions.printer import Printer
import streamlit as st

# MANAGER CLASS

class EnvironmentalMonitorManager:
    """
    Orchestrates the environmental monitoring workflow: planning, data collection,
    analysis, and report writing.
    """

    def __init__(self) -> None:
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, location: str, primary_concern: str = None) -> None:
        # Simplified trace - removed the trace_id and trace functionality
        # self.printer.update_item("start", f"Starting environmental assessment for {location}...", is_done=True)
        st.write(f"Starting environmental assessment for {location}...")

        # Create a site profile with basic information
        site_profile = await self._get_site_profile(location)

        # Develop monitoring plan
        concern_info = f" with focus on {primary_concern}" if primary_concern else ""
        monitoring_plan = await self._create_monitoring_plan(location, site_profile, primary_concern)

        # Collect environmental data
        environmental_data = await self._collect_data(location, monitoring_plan)

        # Integrated analysis
        analysis = await self._analyze_data(location, site_profile, monitoring_plan, environmental_data)

        # Generate comprehensive report
        report = await self._write_report(site_profile, monitoring_plan, environmental_data, analysis)

        status_summary = f"Environmental status for {location}{concern_info}: {self._extract_status(report)}"
        
        # self.printer.update_item("final_status", status_summary, is_done=True)
        st.write(status_summary)

        # self.printer.end()

        # Print final outputs
        # print("\n\n=====ENVIRONMENTAL ASSESSMENT REPORT=====\n\n")
        # print(report)
        st.write("\n\n=====ENVIRONMENTAL ASSESSMENT REPORT=====\n\n")
        st.write(report)

    def _extract_status(self, report: str) -> str:
        """Extract status from report text."""
        if "ENVIRONMENTAL STATUS:" in report:
            lines = report.split("ENVIRONMENTAL STATUS:")[1].split("\n")
            if lines:
                return lines[0].strip()
        return "Assessment completed"

    async def _get_site_profile(self, location: str) -> dict:
        """Generate basic profile information about the site."""
        # self.printer.update_item("profiling", f"Building site profile for {location}...")
        st.write(f"Building site profile for {location}...")

        # Use the data agent to find basic information about the location
        prompt = f"Find basic environmental information about {location} including ecosystem type, region, any known environmental issues, protected species, and historical environmental context."
        result = await Runner.run(data_agent, prompt)
        data_text = str(result.final_output)

        # Parse the information into a simple dictionary instead of using Pydantic models
        site_profile = {
            "site_name": location,
            "data": data_text
        }

        # self.printer.mark_item_done("profiling")
        return site_profile

    async def _create_monitoring_plan(self, location: str, site_profile: dict, primary_concern: str = None) -> dict:
        """Create a monitoring plan based on site profile and primary concern."""
        # self.printer.update_item("planning", "Developing environmental monitoring plan...")
        st.write(f"Developing environmental monitoring plan...")


        # Build prompt based on site information and concerns
        concern_text = f" with particular focus on {primary_concern}" if primary_concern else ""
        prompt = (
            f"Create an environmental monitoring plan for {location}{concern_text}.\n"
            f"Site information:\n{site_profile['data']}\n"
        )

        result = await Runner.run(planner_agent, prompt)
        plan = str(result.final_output)

        # self.printer.update_item(
        #     "planning",
        #     f"Environmental monitoring plan created",
        #     is_done=True,
        # )
        return {"plan": plan}

    async def _collect_data(self, location: str, monitoring_plan: dict) -> List[str]:
        """Collect environmental data based on the monitoring plan."""
        # self.printer.update_item("data_collection", "Collecting environmental data...")
        st.write("Collecting environmental data...")

        # Extract data sources and metrics from the monitoring plan text
        plan_text = monitoring_plan["plan"]

        # Simple extraction of data sources and metrics
        data_queries = []
        if "data sources" in plan_text.lower():
            for line in plan_text.split("\n"):
                if line.strip().startswith("- ") or line.strip().startswith("* "):
                    data_queries.append(f"Find environmental data about {line.strip()[2:]} for {location}")

        # If no specific queries found, use generic ones
        if not data_queries:
            data_queries = [
                f"Find air quality data for {location}",
                f"Find water quality data for {location}",
                f"Find biodiversity data for {location}"
            ]

        # Limit queries to reduce costs
        data_queries = data_queries[:3]  # Limit to maximum 3 queries

        # Run data collection tasks in parallel
        tasks = [asyncio.create_task(self._get_data(query)) for query in data_queries]
        results: list[str] = []
        num_completed = 0

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            # self.printer.update_item(
            #     "data_collection", f"Collecting data... {num_completed}/{len(tasks)} sources completed"
            # )

        # self.printer.mark_item_done("data_collection")


        return results

    async def _get_data(self, query: str) -> str | None:
        """Execute a single data collection query."""
        try:
            result = await Runner.run(data_agent, query)
            return str(result.final_output)
        except Exception:
            return None

    async def _analyze_data(
        self,
        location: str,
        site_profile: dict,
        monitoring_plan: dict,
        environmental_data: List[str]
    ) -> str:
        """Analyze environmental data using the combined analysis agent."""
        # self.printer.update_item("analyzing", "Analyzing environmental data...")
        st.write("Analyzing environmental data...")

        # Prepare input for analysis
        input_data = (
            f"Location: {location}\n"
            f"Site information: {site_profile['data'][:500]}...\n"  # Truncate to save tokens
            f"Monitoring plan: {monitoring_plan['plan'][:500]}...\n"  # Truncate to save tokens
            f"\nEnvironmental data collected:\n"
        )

        # Add environmental data with reasonable limitations
        for i, data in enumerate(environmental_data):
            input_data += f"\nData Source {i+1}:\n{data[:1000]}...\n"  # Limit each data source

        result = await Runner.run(analysis_agent, input_data)
        analysis = str(result.final_output)
        # self.printer.mark_item_done("analyzing")
        return analysis

    async def _write_report(
        self,
        site_profile: dict,
        monitoring_plan: dict,
        environmental_data: List[str],
        analysis: str
    ) -> str:
        """Generate comprehensive environmental report."""
        # self.printer.update_item("reporting", "Drafting environmental report...")
        st.write("Drafting environmental report...")

        # Prepare input for the report writer
        input_data = (
            f"Site: {site_profile['site_name']}\n"
            f"Site information: {site_profile['data'][:500]}...\n"  # Truncate to save tokens
            f"Monitoring plan: {monitoring_plan['plan'][:500]}...\n"  # Truncate to save tokens
            f"\nAnalysis of environmental data:\n{analysis}\n"
            f"\nPlease create a comprehensive environmental report with executive summary, "
            f"environmental status assessment, key indicators, detailed findings, recommendations, "
            f"and data gaps."
        )

        result = await Runner.run(writer_agent, input_data)
        report = str(result.final_output)
        # self.printer.mark_item_done("reporting")
        return report


async def main() -> None:
    """Main entry point for the environmental monitoring system."""
    st.title("Environmental Monitoring and Sustainability Assessment System")
    st.markdown("""
        This system helps assess the environmental status of a given location by collecting data, analyzing it,
        and generating a comprehensive report. You can enter a location and, optionally, specify a primary environmental concern (e.g., deforestation, pollution) to focus the assessment.
    """)
    location = st.text_input("Enter location to assess:")
    concern = st.text_input("Enter primary environmental concern (optional):")
    if st.button("Start Assessment"):
        mgr = EnvironmentalMonitorManager()
        await mgr.run(location, concern if concern else None)


# Start the Chainlit app
if __name__ == "__main__":
   asyncio.run(main())
    #  main()