import os
import sys
import json
from dotenv import load_dotenv
from typing import List, Dict, Any
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()


class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]


class AIAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.messages: List[Dict[str, str]] = []
        self.tools: Dict[str, Tool] = {}
        self._setup_tools()
        print("AI Agent initialized ")

    def _setup_tools(self):
        self.tools = {
            "read_file": Tool(
                name="read_file",
                description="Use this tool to read the contents of a file.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to read.",
                        }
                    },
                    "required": ["path"],
                },
            ),
            "list_files": Tool(
                name="list_files",
                description="Use this tool to list all files in a directory.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the directory to list files from.",
                        }
                    },
                    "required": ["path"],
                },
            ),
            "edit_file": Tool(
                name="edit_file",
                description="Use this tool to edit a file.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to get information about.",
                        },
                        "old_content": {
                            "type": "string",
                            "description": "The content to be replaced in the file. Leave empty to create a new file",
                        },
                        "new_content": {
                            "type": "string",
                            "description": "The new content to replace the old content with.",
                        },
                    },
                    "required": ["path", "new_content"],
                },
            ),
        }

    def _read_file(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            return f"Contents of the file {path}:\n{content} "
        except FileNotFoundError:
            return f"Error: The file at {path} was not found."
        except Exception as e:
            return f"An error occurred while reading the file: {str(e)}"

    def _list_files(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                return f"Error: The directory at {path} does not exist."

            items = []
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"[DIR] {item}/")
                else:
                    items.append(f"[FILE] {item}")

            return f"Files in directory {path}:\n" + "\n".join(items)
        except FileNotFoundError:
            return f"Error: The directory at {path} was not found."
        except Exception as e:
            return f"An error occurred while listing files: {str(e)}"

    def _edit_file(self, path: str, old_content: str, new_content: str) -> str:
        try:
            if os.path.exists(path) and old_content:
                with open(path, "r", encoding="utf-8") as file:
                    current_content = file.read()
                if old_content and old_content not in current_content:
                    return f"Error: The specified old content was not found in the file {path}."

                content = current_content.replace(old_content, new_content)
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)

                return f"File {path} has been successfully updated."
            else:
                # Only create directory if path contains sub directories
                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)

                return f"File {path} has been successfully created."
        except Exception as e:
            return f"An error occurred while editing the file: {str(e)}"

    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        try:
            if tool_name == "read_file":
                return self._read_file(parameters["path"])
            elif tool_name == "list_files":
                return self._list_files(parameters["path"])
            elif tool_name == "edit_file":
                return self._edit_file(
                    parameters["path"],
                    parameters.get("old_content", ""),
                    parameters["new_content"],
                )
            else:
                return f"Error: Tool {tool_name} is not recognized."
        except Exception as e:
            return f"Error: Error occurred while executing tool {tool_name}."

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        # Format tools for OpenAI API
        tool_schemas = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                },
            }
            for tool in self.tools.values()
        ]

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=self.messages,
                    tools=tool_schemas,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=1500,
                )

                assistant_message = response.choices[0].message
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": assistant_message.tool_calls,
                    }
                )
                print(f"Assistant message: {assistant_message}")
                # Check if the assistant wants to call tools
                if assistant_message.tool_calls:
                    # Execute each tool call
                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)

                        # Execute the tool
                        tool_result = self._execute_tool(tool_name, tool_args)

                        # Add tool result to messages
                        self.messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": tool_result,
                            }
                        )

                    # Continue the loop to get the final response
                    continue
                else:
                    # No tool calls, return the assistant's response
                    return (
                        assistant_message.content
                        or "I apologize, but I couldn't generate a response."
                    )

            except Exception as e:
                return f"An error occurred during chat completion: {str(e)}"

        return "Maximum iterations reached. The conversation may be too complex."


if __name__ == "__main__":
    print("Starting AI Agent...")
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API key found: {'Yes' if api_key else 'No'}")

    if not api_key:
        print("Error: OPENAI_API_KEY is not set in environment variables.")
        sys.exit(1)

    agent = AIAgent(api_key=api_key)
    # test the tool
    print("Sending chat message...")
    response = agent.chat("Hello, list the current directory.")
    print("Response received:")
    print(response)
