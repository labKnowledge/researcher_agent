# Web Research Agent

A web research agent built with the Agent-to-Agent (A2A) protocol that performs comprehensive web searches using DuckDuckGo and returns detailed results with cited sources.

## Features

- Web research through DuckDuckGo search
- Comprehensive summaries of search results
- Cited sources with each research response
- A2A protocol compatible for integration with other agents
- Configurable API endpoint serving research capabilities

## Installation

### Prerequisites

- Python 3.12 or higher
- [Google API key](https://console.cloud.google.com/) for Gemini model access

### Setup

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd researcher
   ```

2. Set up a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -e .
   ```

4. Create a `.env` file in the project root with your API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

### Running the server

Start the research agent server:

```bash
python -m researcher
```

This will start the server on `http://localhost:10011/` by default.

### Configuration options

You can specify host and port:

```bash
python -m researcher --host 0.0.0.0 --port 8080
```

### Docker deployment

Build and run the Docker container:

```bash
docker build -t research-agent .
docker run -p 10011:10011 -e GOOGLE_API_KEY=your_google_api_key_here research-agent
```

## Agent Capabilities

- **Research Topics**: The agent can research any topic using web searches and provide comprehensive summaries.
- **Cited Sources**: All research results include cited sources for reference.
- **A2A Integration**: Compatible with other agents using the Agent-to-Agent protocol.

## Architecture

This research agent uses:

- [CrewAI](https://github.com/joaomdmoura/crewai) for agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) for web search tools
- [Agent-to-Agent Protocol](https://github.com/a2a-research/agent-protocol) for standardized agent communication

## License

[License information]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
