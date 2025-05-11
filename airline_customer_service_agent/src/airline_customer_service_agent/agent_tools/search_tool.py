import requests
from agents import function_tool
from pydantic import BaseModel
from models.airline_models import SearchQuery
import os
from dotenv import load_dotenv

_ = load_dotenv()

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

@function_tool
async def serper_search(input: SearchQuery) -> str:
    """Search the web using Serper.dev and return the top results."""

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": input.query,
        "gl": "us",
        "hl": "en"
    }

    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)

    if response.status_code != 200:
        return f"Failed to fetch search results. Status: {response.status_code}"

    results = response.json()
    organic = results.get("organic", [])

    if not organic:
        return "No results found."

    top_results = []
    for r in organic[:3]:
        title = r.get("title", "")
        link = r.get("link", "")
        snippet = r.get("snippet", "")
        top_results.append(f"🔗 {title}\n{snippet}\n{link}")

    return "\n\n".join(top_results)
