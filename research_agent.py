"""Research Agent based on CrewAI for A2A protocol.

Provides research capabilities using DuckDuckGo search.
"""

import asyncio
import os
from typing import Any, AsyncIterable, Dict, List
from uuid import uuid4
import logging
from pydantic import BaseModel
from dotenv import load_dotenv

from crewai import Agent, Crew, Task, LLM
from crewai.process import Process
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

logger = logging.getLogger(__name__)

class ResearchResult(BaseModel):
    """Represents research results.

    Attributes:
        id: Unique identifier for the research result
        content: Textual content of the research
        sources: List of sources referenced
        error: Error message if there was an issue
    """

    id: str = None
    content: str = None
    sources: List[str] = None
    error: str = None


def get_api_key() -> str:
    """Helper method to handle API Key."""
    load_dotenv()
    return os.getenv("DASH_API_KEY")


# Create a custom CrewAI tool that wraps DuckDuckGoSearchRun
class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search"
    description: str = "Search the web for information about a specific topic."
    
    def _run(self, query: str) -> str:
        """Execute the search with the given query."""
        search_tool = DuckDuckGoSearchRun()
        return search_tool.run(query)


class ResearchAgent:
    """Agent that performs research using DuckDuckGo."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        self.model = LLM(model="openai/qwen-plus", api_key=get_api_key(), base_url=os.getenv("DASH_BASE_URL"))
        # Create the custom DuckDuckGo search tool
        self.search_tool = DuckDuckGoSearchTool()

        self.researcher_agent = Agent(
            role="Research Expert",
            goal=(
                "Research topics thoroughly using DuckDuckGo search and provide comprehensive "
                "but concise summaries with relevant information and sources."
            ),
            backstory=(
                "You are an expert researcher with years of experience finding and synthesizing "
                "information from the web. You excel at formulating effective search queries, "
                "extracting key information, and presenting findings in a clear and structured way."
            ),
            verbose=False,
            allow_delegation=False,
            tools=[self.search_tool],
            llm=self.model,
        )

        self.research_task = Task(
            description=(
                "Research the topic: '{research_query}'\n"
                "1. Start by formulating 2-3 specific search queries based on the topic\n"
                "2. Use the DuckDuckGo search tool to find relevant information\n"
                "3. Synthesize a comprehensive but concise summary of the findings\n"
                "4. Include key facts, different perspectives, and recent developments\n"
                "5. List all sources consulted at the end of your response"
            ),
            expected_output=(
                "A comprehensive research summary with cited sources that directly "
                "addresses the query with accurate and up-to-date information."
            ),
            agent=self.researcher_agent,
        )

        self.research_crew = Crew(
            agents=[self.researcher_agent],
            tasks=[self.research_task],
            process=Process.sequential,
            verbose=False,
        )

    def invoke(self, query, session_id) -> ResearchResult:
        """Kickoff CrewAI research and return the response."""
        try:
            logger.info(f"Starting research on: {query}")
            inputs = {"research_query": query}
            response = self.research_crew.kickoff(inputs)
            
            # Extract sources from the response text
            sources = []
            content = response.raw
            
            # Simple extraction of URLs or references
            # This could be enhanced with better parsing
            if "Sources:" in content:
                main_content, sources_section = content.split("Sources:", 1)
                content = main_content.strip()
                sources = [s.strip() for s in sources_section.strip().split("\n") if s.strip()]
            
            return ResearchResult(
                id=uuid4().hex,
                content=content,
                sources=sources
            )
        except Exception as e:
            logger.error(f"Error during research: {e}")
            return ResearchResult(
                id=uuid4().hex,
                error=f"Error performing research: {str(e)}"
            )

    async def stream(self, query: str) -> AsyncIterable[Dict[str, Any]]:
        """Streaming is not supported by CrewAI."""
        raise NotImplementedError("Streaming is not supported by CrewAI.") 