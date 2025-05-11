import asyncio
import time
from collections.abc import Sequence
from rich.console import Console
from agents import Runner
from helper_functions.printer import Printer
from helper_functions.utils import _summary_extractor
import chainlit as cl
from multi_agents import (
    planner_agent,
    search_agent,
    risk_agent,
    writer_agent,
    financials_agent,
    verifier_agent
)
from models.financial_models import (
    FinancialSearchPlan,
    FinancialSearchItem,
    FinancialReportData,
    VerificationResult
)


class FinancialResearchManager:
    """
    Orchestrates the full flow: planning, searching, sub‑analysis, writing, and verification.
    """

    def __init__(self) -> None:
        pass

    async def run(self, query: str) -> None:
        # Initial message
        start_msg = await cl.Message(content="Starting financial research...").send()

        # Plan searches
        search_plan = await self._plan_searches(query)

        # Perform searches
        search_results = await self._perform_searches(search_plan)

        # Write the report
        report = await self._write_report(query, search_results)

        # Verification of the report
        verification = await self._verify_report(report)

        # Final report summary
        final_report = f"Report summary\n\n{report.short_summary}"
        await cl.Message(content=final_report).send()

        # Send report and follow-up questions
        await cl.Message(content=f"Report:\n{report.markdown_report}").send()
        await cl.Message(content="=====FOLLOW UP QUESTIONS=====").send()
        await cl.Message(content="\n".join(report.follow_up_questions)).send()

        # Send verification results
        await cl.Message(content="=====VERIFICATION=====").send()
        # Assuming 'verification' is a sequence of tuples, convert each item to a string
        verification_text = "\n".join(f"{key}: {value}" for key, value in verification)
        await cl.Message(content=verification_text).send()


    async def _plan_searches(self, query: str) -> FinancialSearchPlan:
        await cl.sleep(2)
        await cl.Message(content="Planning searches...").send()
        result = await Runner.run(planner_agent, f"Query: {query}")
        await cl.Message(content=f"Will perform {len(result.final_output.searches)} searches").send()
        return result.final_output_as(FinancialSearchPlan)

    async def _perform_searches(self, search_plan: FinancialSearchPlan) -> Sequence[str]:
        # Create a message to update search progress
        progress_msg = await cl.Message(content="Searching... 0/0 completed").send()

        tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
        results: list[str] = []
        num_completed = 0

        # Process the search tasks and update the progress message
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                results.append(result)
            num_completed += 1

            # Update the progress dynamically using msg.update()
            progress_msg.content = f"Searching... {num_completed}/{len(tasks)} completed"
            await progress_msg.update()

        # Final update when search is done
        progress_msg.content = f"Searching... {len(tasks)}/{len(tasks)} completed - Done!"
        await progress_msg.update()

        return results

    async def _search(self, item: FinancialSearchItem) -> str | None:
        input_data = f"Search term: {item.query}\nReason: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_data)
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: Sequence[str]) -> FinancialReportData:
        fundamentals_tool = financials_agent.as_tool(
            tool_name="fundamentals_analysis",
            tool_description="Use to get a short write‑up of key financial metrics",
            custom_output_extractor=_summary_extractor,
        )
        risk_tool = risk_agent.as_tool(
            tool_name="risk_analysis",
            tool_description="Use to get a short write‑up of potential red flags",
            custom_output_extractor=_summary_extractor,
        )
        writer_with_tools = writer_agent.clone(tools=[fundamentals_tool, risk_tool])

        input_data = f"Original query: {query}\nSummarized search results: {search_results}"

        # Create a message to indicate the report is being written
        thinking_msg = await cl.Message(content="Thinking about report...").send()

        result = Runner.run_streamed(writer_with_tools, input_data)

        # Update the thinking message while writing
        async for _ in result.stream_events():
            thinking_msg.content = "Thinking about report..."
            await thinking_msg.update()

        # Finalize the thinking message
        thinking_msg.content = "Thinking about report... Done!"
        await thinking_msg.update()

        return result.final_output_as(FinancialReportData)

    async def _verify_report(self, report: FinancialReportData) -> VerificationResult:
        # Create a message for verification
        verification_msg = await cl.Message(content="Verifying report...").send()
        result = await Runner.run(verifier_agent, report.markdown_report)
        verification_msg.content = "Verifying report... Done!"
        await verification_msg.update()
        return result.final_output_as(VerificationResult)

@cl.on_chat_start
async def on_chat_start():
    # Initialize session state
    cl.user_session.set("research_manager", FinancialResearchManager())
    
    # Welcome message
    await cl.Message(
        content="""# Financial Research Assistant
        
Welcome! I can help you research financial information about companies and markets.
        
Ask me about a company, industry, or financial trend, and I'll provide a detailed analysis."""
    ).send()


# Define Chainlit message handler
@cl.on_message
async def handle_query(message: str):
    mgr = FinancialResearchManager()
    await mgr.run(message.content)

# Start the Chainlit app
if __name__ == "__main__":
    cl.run(handle_query)
