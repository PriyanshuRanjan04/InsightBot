import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.tools.tavily_search import TavilySearchResults
from config.config import TAVILY_API_KEY, MAX_SEARCH_RESULTS

def get_web_search_results(query):
    """Perform live web search using Tavily and return results"""
    try:
        os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
        
        search_tool = TavilySearchResults(
            max_results=MAX_SEARCH_RESULTS
        )
        
        results = search_tool.invoke(query)
        
        if not results:
            return "No web search results found."
        
        formatted = ""
        for i, result in enumerate(results, 1):
            formatted += f"**Result {i}:**\n"
            formatted += f"- **Title:** {result.get('title', 'N/A')}\n"
            formatted += f"- **URL:** {result.get('url', 'N/A')}\n"
            formatted += f"- **Content:** {result.get('content', 'N/A')}\n\n"
        
        return formatted

    except Exception as e:
        raise RuntimeError(f"Failed to perform web search: {str(e)}")