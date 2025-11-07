# First Agent

This project is a research assistant agent built with LangChain and OpenAI. It can use tools like DuckDuckGo Search and Wikipedia to answer user queries and save the research output to a file.

## Features

-   **Research Assistant Agent:** An AI agent that can understand and respond to user queries.
-   **Tool Integration:** The agent can use external tools to gather information.
    -   **DuckDuckGo Search:** For searching the web for current information.
    -   **Wikipedia:** For querying Wikipedia for encyclopedic information.
    -   **Save Tool:** For saving the research output to a timestamped text file.
-   **Structured Output:** The agent provides a structured response in JSON format, which includes the topic, a summary of the research, a list of sources, and the tools used.
-   **Command-Line Interface:** The project provides a simple command-line interface to interact with the agent.

## Getting Started

### Prerequisites

-   Python 3.13 or higher
-   An OpenAI API key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/first-agent.git
    cd first-agent
    ```

2.  **Install the dependencies:**

    The project uses `uv` for package management. If you don't have `uv` installed, you can install it with `pip`: `pip install uv`.

    ```bash
    uv pip install -r requirements.txt
    ```
    
    *Note: A `requirements.txt` file is not provided. You can install dependencies directly from `pyproject.toml` if you are using a compatible package manager or generate a `requirements.txt` file.*

3.  **Set up the environment variables:**

    Create a `.env` file in the root directory of the project and add your OpenAI API key:

    ```
    OPENAI_API_KEY="your-openai-api-key"
    ```

## Usage

To run the research assistant agent, execute the `main.py` script:

```bash
python main.py
```

The script will prompt you to enter your research query. The agent will then process the query, use the available tools to gather information, and print the research output to the console.

### Example

```
Enter your research query: What is the population of Tokyo?

🔍 Processing query: 'What is the population of Tokyo?'
📡 Invoking agent with tools...
=== Tool Usage Summary ===
Tools used by agent:
  {'name': 'search', 'args': {'query': 'current population of Tokyo'}, 'id': 'call_abc123'}
=== Agent Made 1 Tool Call(s) ===
=== Successfully Parsed Structured Response ===
Topic: Population of Tokyo
Summary: As of 2024, the estimated population of the Tokyo metropolitan area is over 37 million people, making it the largest metropolitan area in the world.
Sources: ['https://www.worldometers.info/world-population/japan-population/']
Tools used: ['search']

Tool calling agent with empty tools list worked successfully!
PydanticOutputParser successfully parsed the structured response!
```

## Tools

The project uses the following tools:

-   **`search_tool`:** This tool uses the DuckDuckGo Search API to search the web for information.
-   **`wiki_tool`:** This tool uses the Wikipedia API to query Wikipedia for information.
-   **`save_tool`:** This tool saves the research output to a timestamped text file.

## Dependencies

The project's dependencies are listed in the `pyproject.toml` file:

-   `ddgs>=9.7.0`
-   `langchain>=1.0.3`
-   `langchain-anthropic>=1.0.1`
-   `langchain-community>=0.4.1`
-   `langchain-core>=1.0.2`
-   `langchain-openai>=1.0.1`
-   `pydantic>=2.12.3`
-   `python-dotenv>=1.2.1`
-   `wikipedia>=1.4.0`
