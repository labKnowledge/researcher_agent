"""This file serves as the main entry point for the Research agent application.

It initializes the A2A server, defines the agent's capabilities,
and starts the server to handle incoming requests.
"""

from research_agent import ResearchAgent
import click
from agent2agent.server import A2AServer
from agent2agent.types import AgentCapabilities, AgentCard, AgentSkill, MissingAPIKeyError
import logging
import os
from research_task_manager import ResearchTaskManager
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=8099)  # Different port than the image generator
def main(host, port):
    """Entry point for the A2A + CrewAI Research Agent sample."""
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")

        capabilities = AgentCapabilities(streaming=False)
        skill = AgentSkill(
            id="web_researcher",
            name="Web Researcher",
            description=(
                "Research topics on the web using DuckDuckGo search and provide "
                "comprehensive summaries with relevant information and sources."
            ),
            tags=["research", "web search", "information gathering"],
            examples=[
                "Research the latest developments in quantum computing", 
                "Find information about climate change solutions",
                "Gather data on renewable energy trends"
            ],
        )

        agent_card = AgentCard(
            name="Research Agent",
            description=(
                "A powerful research assistant that can search the web for information "
                "on any topic and provide comprehensive summaries with cited sources."
            ),
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=ResearchAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=ResearchAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        server = A2AServer(
            agent_card=agent_card,
            task_manager=ResearchTaskManager(agent=ResearchAgent()),
            host=host,
            port=port,
        )
        logger.info(f"Starting Research Agent server on {host}:{port}")
        server.start()
    except MissingAPIKeyError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main() 