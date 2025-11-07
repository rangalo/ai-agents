# AI Agent Without Framework

This project is a conversational AI agent that can read, list, and edit files on your local system. It is built from scratch in Python without using any external frameworks like LangChain or LlamaIndex. This project is intended to be a learning exercise for understanding the core concepts of building AI agents.

## Features

- **Conversational AI:** The agent can understand and respond to user input in a conversational manner.
- **Tool Usage:** The agent can use tools to interact with the local file system, including:
    - `read_file`: Read the contents of a file.
    - `list_files`: List all files in a directory.
    - `edit_file`: Edit the contents of a file.
- **Extensible:** The agent's capabilities can be extended by adding new tools.
- **Interactive Chat:** The agent can be run in an interactive chat mode in the terminal.

## Getting Started

### Prerequisites

- Python 3.7+
- An OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/agent-without-framework.git
   ```
2. Install the dependencies:
   ```bash
   uv sync
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key
   ```

### Usage

To run the agent in interactive chat mode, run the following command:

```bash
python main.py
```

You can then start a conversation with the agent in the terminal. To exit the chat, type `exit` or `quit`.

## Project Structure

The project is structured as follows:

- `main.py`: The main entry point for the application.
- `runbook/`: A directory containing a series of Python scripts that build up the agent's functionality step-by-step.
    - `01_basic_script.py`: A basic script that loads the environment variables.
    - `02_agent_class.py`: Defines the `AIAgent` class.
    - `03_define_tools.py`: Defines the tools that the agent can use.
    - `04_tools_execution.py`: Implements the tool execution logic.
    - `05_chat_method.py`: Implements the `chat` method for the agent.
    - `06_interactive_chat.py`: Implements the interactive chat mode.
    - `07_adding_personality.py`: Adds a personality to the agent.
- `pyproject.toml`: A file containing the project's dependencies.
- `README.md`: This file.

## How It Works

The agent is built around the `AIAgent` class, which is responsible for managing the conversation and executing tools. The `AIAgent` class uses the OpenAI API to generate responses to user input. When the user's input requires the use of a tool, the agent calls the appropriate tool and uses the tool's output to generate a response.

The agent's tools are defined in the `_setup_tools` method of the `AIAgent` class. Each tool is defined by a name, a description, and an input schema. The agent uses the tool's description to determine when to use the tool, and it uses the input schema to validate the tool's input.

The agent's chat logic is implemented in the `chat` method of the `AIAgent` class. The `chat` method takes the user's input as input and returns the agent's response. The `chat` method uses a `while` loop to allow the agent to make multiple tool calls in a single turn.

## Conclusion

This project provides a basic framework for building AI agents without using any external frameworks. The project is intended to be a starting point for building more complex and sophisticated agents.
