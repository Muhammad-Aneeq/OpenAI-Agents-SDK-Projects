import os
from typing import Any, Dict, List
from agents import RunContextWrapper, function_tool
from models.content import ContentContext
import requests
import os
from dotenv import load_dotenv
    
load_dotenv()

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")


@function_tool
async def research_topic(
    wrapper: RunContextWrapper[ContentContext]
) -> Dict[str, Any]:
    """Research a blog topic and gather relevant information using Serper API"""
    print("Starting research on topic...")

    title = wrapper.context["title"]
    keywords = wrapper.context["keywords"]
    target_audience = wrapper.context["target_audience"]

    if not SERPER_API_KEY:
        print("Warning: SERPER_API_KEY not found in environment variables")
        return {"error": "SERPER_API_KEY not configured"}
    
    # Collect search results for both the title and each keyword
    search_results = []

    # Search for the main title
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    primary_query = title
    print(f"Searching for: {primary_query}")

    payload = {
        "q": primary_query,
        "gl": "us",
        "hl": "en"
    }
        
    try:
        response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
        response.raise_for_status()
        results = response.json()
        
        organic = results.get("organic", [])
        for r in organic[:5]:  # Get top 5 results
            title = r.get("title", "")
            link = r.get("link", "")
            snippet = r.get("snippet", "")
            search_results.append({
                "title": title,
                "url": link,
                "snippet": snippet,
                "query": primary_query
            })
    except Exception as e:
        print(f"Error searching for main title: {e}")

    
    # Now search for each keyword to gather diverse information
    for keyword in keywords[:3]:  # Limit to first 3 keywords to avoid too many requests
        keyword_query = keyword
        print(f"Searching for keyword: {keyword_query}")
        
        payload = {
            "q": keyword_query,
            "gl": "us",
            "hl": "en"
        }
        
        try:
            response = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
            response.raise_for_status()
            results = response.json()
            
            organic = results.get("organic", [])
            for r in organic[:3]:  # Get top 3 results per keyword
                title = r.get("title", "")
                link = r.get("link", "")
                snippet = r.get("snippet", "")
                search_results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                    "query": keyword_query
                })
        except Exception as e:
            print(f"Error searching for keyword {keyword}: {e}")
    
    # Structure the research data based on the search results
    research_data = {
        "topic_overview": f"Research data for: {title}",
        "search_results": search_results,
        "key_points": [
            f"Information gathered from searches on {title} and related keywords",
            f"Content targeted for audience: {target_audience}",
            f"Multiple sources searched with keywords: {', '.join(keywords[:3])}"
        ],
        "resources": [{"title": result["title"], "url": result["url"]} for result in search_results[:5]],
        "completion_status": "complete"
    }

    # Update the context with the research data
    wrapper.context["research_data"] = research_data
    
    print("Research completed.")
    
    return research_data
