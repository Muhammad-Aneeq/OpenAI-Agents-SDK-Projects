from pydantic import BaseModel

# MODELS FOR DATA STRUCTURES

class SearchQuery(BaseModel):
    query: str

class LiteratureSearchItem(BaseModel):
    reason: str
    """Reasoning for why this search term is relevant."""

    query: str
    """The search term to feed into academic search engines."""

class LiteratureSearchPlan(BaseModel):
    searches: list[LiteratureSearchItem]
    """List of searches to perform."""

class AnalysisSummary(BaseModel):
    summary:  str
    """Short text summary for this aspect of the analysis."""

class ResearchReportData(BaseModel):
    short_summary: str
    """A concise abstract of the findings (2-3 sentences)."""

    markdown_report: str
    """The full scholarly report in markdown format."""

    future_research: list[str]
    """Suggested directions for future research."""

class VerificationResult(BaseModel):
    verified: bool
    """Whether the report meets academic standards."""

    issues: str
    """If not verified, describe the main issues or concerns."""
