#!/usr/bin/env python3
"""
Web Search Tool for LangChain ReAct Agent
Provides web search capability using DuckDuckGo
"""

from typing import Optional, List, Dict
from langchain.tools import BaseTool
from pydantic import Field

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None


class WebSearchTool(BaseTool):
    """Tool for searching the web using DuckDuckGo"""
    
    name: str = "web_search"
    description: str = """Useful for searching the web to find current information, facts, or answers.
    Input should be a search query as a string.
    Returns the top search results with titles, snippets, and URLs.
    
    Examples:
    - "latest Python version 2026"
    - "LangChain documentation"
    - "IBM Granite model features"
    - "weather in New York"
    - "current events technology"
    
    Use this tool when you need to find information that you don't already know,
    or when you need current/recent information.
    """
    
    max_results: int = Field(default=5, description="Maximum number of results to return")
    
    def _search_duckduckgo(self, query: str) -> List[Dict[str, str]]:
        """
        Perform a DuckDuckGo search
        
        Args:
            query: Search query string
            
        Returns:
            List of search results with title, snippet, and URL
        """
        if DDGS is None:
            return [{
                "title": "Error",
                "snippet": "DuckDuckGo search library not installed. Install with: pip install duckduckgo-search",
                "url": ""
            }]
        
        try:
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=self.max_results)
                
                for result in search_results:
                    results.append({
                        "title": result.get("title", "No title"),
                        "snippet": result.get("body", "No description"),
                        "url": result.get("href", "")
                    })
            
            return results if results else [{
                "title": "No results",
                "snippet": f"No search results found for: {query}",
                "url": ""
            }]
            
        except Exception as e:
            return [{
                "title": "Search Error",
                "snippet": f"Error performing search: {str(e)}",
                "url": ""
            }]
    
    def _format_results(self, results: List[Dict[str, str]]) -> str:
        """
        Format search results for display
        
        Args:
            results: List of search result dictionaries
            
        Returns:
            Formatted string of results
        """
        if not results:
            return "No results found."
        
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"{i}. {result['title']}")
            formatted.append(f"   {result['snippet']}")
            if result['url']:
                formatted.append(f"   URL: {result['url']}")
            formatted.append("")  # Empty line between results
        
        return "\n".join(formatted)
    
    def _run(self, query: str) -> str:
        """
        Execute the web search tool
        
        Args:
            query: Search query string
            
        Returns:
            Formatted search results or error message
        """
        try:
            query = query.strip()
            
            if not query:
                return "Error: Search query cannot be empty"
            
            # Perform the search
            results = self._search_duckduckgo(query)
            
            # Format and return results
            formatted_results = self._format_results(results)
            
            return f"Search results for '{query}':\n\n{formatted_results}"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of _run"""
        return self._run(query)


# Example usage and testing
if __name__ == "__main__":
    tool = WebSearchTool(max_results=3)
    
    print("Web Search Tool Test Cases:")
    print("=" * 70)
    
    # Test cases
    test_queries = [
        "LangChain framework",
        "IBM Granite AI model",
        "Python latest version",
    ]
    
    for query in test_queries:
        print(f"\nSearching for: {query}")
        print("-" * 70)
        result = tool._run(query)
        print(result)
        print()

# Made with Bob
