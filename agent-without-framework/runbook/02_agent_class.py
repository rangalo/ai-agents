import os
import sys
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
        print("AI Agent initialized ")


if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is not set in environment variables.")
        sys.exit(1)

    agent = AIAgent(api_key=api_key)
