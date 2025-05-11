from dataclasses import dataclass
from typing import Any, Dict, Optional, List


@dataclass
class ContentContext:
    title: str
    keywords: List[str]
    target_audience: str
    research_data: Optional[Dict[str, Any]]
    content_draft: Optional[str]