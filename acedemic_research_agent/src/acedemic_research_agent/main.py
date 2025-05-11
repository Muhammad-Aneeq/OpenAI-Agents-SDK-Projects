from __future__ import annotations
import asyncio
import time
from collections.abc import Sequence
from typing import Any
from pydantic import BaseModel
from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner
import chainlit as cl
from agents import Runner, RunResult
from agents.model_settings import ModelSettings
from models.acedemic_models import (
    LiteratureSearchPlan,
    LiteratureSearchItem,
    ResearchReportData,
    VerificationResult
)
from multi_agent import (
    planner_agent,
    search_agent,
    writer_agent,
    methodology_agent,
    theory_agent,
    verifier_agent
)

async def _summary_extractor(run_result: RunResult) -> str:
    """Custom output extractor for sub-agents that return an AnalysisSummary."""
    return str(run_result.final_output.summary)


class AcademicResearchManager:
    """
    Orchestrates the full academic research flow: planning searches,
    gathering literature, analyzing content, writing, and verification.
    """

    def __init__(self) -> None:
        self.console = Console()

    async def run(self, query: str) -> None:
         # Initial message
        start_msg = await cl.Message(content="Starting academic research...").send()

            # Plan the literature search strategy
        search_plan = await self._plan_searches(query)

            # Execute the searches
        search_results = await self._perform_searches(search_plan)

            # Write the comprehensive report
        report = await self._write_report(query, search_results)

            # Verify the report meets academic standards
        verification = await self._verify_report(report)

        final_report = f"Research summary\n\n{report.short_summary}"
        await cl.Message(content=final_report).send()

        # Print final outputs
        await cl.Message(content="=====ACADEMIC REPORT=====").send()
        await cl.Message(content=f"Report:\n{report.markdown_report}").send()
        await cl.Message(content="======FUTURE RESEARCH DIRECTIONS=====").send()
        await cl.Message(content="\n".join(report.future_research)).send()
        await cl.Message(content="======PEER REVIEW ASSESSMENTS=====").send()
        verification_text = "\n".join(f"{key}: {value}" for key, value in verification)
        await cl.Message(content=verification_text).send()
 

    async def _plan_searches(self, query: str) -> LiteratureSearchPlan:
        await cl.sleep(2)
        await cl.Message(content="Planning literature search strategy...").send()
        result = await Runner.run(planner_agent, f"Research topic: {query}")
        await cl.Message(content=f"Identified {len(result.final_output.searches)} relevant search terms").send()
    
        return result.final_output_as(LiteratureSearchPlan)

    async def _perform_searches(self, search_plan: LiteratureSearchPlan) -> Sequence[str]:
         # Create a message to update search progress
        progress_msg = await cl.Message(content="Searching academic literature... 0/0 completed").send()
        tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
        results: list[str] = []
        num_completed = 0

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1

            # Update the progress dynamically using msg.update()
            progress_msg.content = f"Searching academic literature... {num_completed}/{len(tasks)} completed"
            await progress_msg.update()

        # Final update when search is done
        progress_msg.content = f"Searching academic literature... {len(tasks)}/{len(tasks)} completed - Done!"
        return results

    async def _search(self, item: LiteratureSearchItem) -> str | None:
        input_data = f"Academic search term: {item.query}\nRelevance: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_data)
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: Sequence[str]) -> ResearchReportData:
        # Make specialist analyst agents available as tools
        methodology_tool = methodology_agent.as_tool(
            tool_name="methodology_analysis",
            tool_description="Use to get specialized analysis of research methodologies",
            custom_output_extractor=_summary_extractor,
        )

        theory_tool = theory_agent.as_tool(
            tool_name="theory_analysis",
            tool_description="Use to get specialized analysis of theoretical frameworks",
            custom_output_extractor=_summary_extractor,
        )

        writer_with_tools = writer_agent.clone(tools=[methodology_tool, theory_tool])

        # Create a message to indicate the report is being written
        thinking_msg = await cl.Message(content="Analyzing literature and drafting report...").send()

        input_data = f"Research question: {query}\nLiterature search findings: {search_results}"
        result = Runner.run_streamed(writer_with_tools, input_data)

        update_messages = [
            "Organizing research findings...",
            "Drafting literature review...",
            "Synthesizing key insights...",
            "Finalizing academic report...",
        ]

        last_update = time.time()
        next_message = 0
        async for _ in result.stream_events():
            if time.time() - last_update > 5 and next_message < len(update_messages):
                thinking_msg.content = update_messages[next_message]
                await thinking_msg.update()
                next_message += 1
                last_update = time.time()
                
         # Finalize the thinking message
        thinking_msg.content = "writing academic report... Done!"
        await thinking_msg.update()
        return result.final_output_as(ResearchReportData)


    async def _verify_report(self, report: ResearchReportData) -> VerificationResult:
        # Create a message for verification
        verification_msg = await cl.Message(content="Conducting peer review assessment...").send()
        result = await Runner.run(verifier_agent, report.markdown_report)
        verification_msg.content = "Conducting peer review assessment... Done!"
        await verification_msg.update()
        return result.final_output_as(VerificationResult)



@cl.on_chat_start
async def on_chat_start():
    # Initialize session state
    cl.user_session.set("research_manager", AcademicResearchManager())
    
    # Welcome message
    await cl.Message(
    content="""# Academic Research Assistant
        
Welcome! I can help you research academic information about companies, industries, and various market trends.
        
Ask me about a company, industry, academic concept, or research topic, and I'll provide a detailed analysis."""
).send()


# Define Chainlit message handler
@cl.on_message
async def handle_query(message: str):
    mgr = AcademicResearchManager()
    await mgr.run(message.content)

# Start the Chainlit app
if __name__ == "__main__":
    cl.run(handle_query)
