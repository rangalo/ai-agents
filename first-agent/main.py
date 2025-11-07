from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


def main():
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        # Create parser for structured output
        parser = PydanticOutputParser(pydantic_object=ResearchResponse)

        # Create tool calling agent with search tool only (wiki_tool causing issues)
        tools = [search_tool, wiki_tool, save_tool]

        agent = create_agent(
            model=llm,
            system_prompt=f"""You are a research assistant. 

            CRITICAL INSTRUCTION: For ANY user question, you MUST use the search tool to find current information before responding.

            Available tools:
            - search: Use this to find current web information about any topic            
            - wiki: Use this to query Wikipedia for information
            - save: Use this to save research output to a file

            Use necessary tools to gather information.

            {parser.get_format_instructions()}

            IMPORTANT: 
            - Use real URLs from search results for sources
            - Provide only the JSON response after using tools""",
            tools=tools,
        )

        # Enable dynamic input - tools should work now
        query = input("Enter your research query: ")

        print(f"\n🔍 Processing query: '{query}'")
        print("📡 Invoking agent with tools...")

        response = agent.invoke({"messages": [{"role": "user", "content": query}]})

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return
    except Exception as e:
        print(f"❌ Error during agent setup or execution: {e}")
        return

    # Show tool usage clearly
    print("=== Tool Usage Summary ===")
    tool_calls = []
    for message in response["messages"]:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append(tool_call)

    if tool_calls:
        print("Tools used by agent:")
        for call in tool_calls:
            print(f"  {call}")
    else:
        print("❌ No tools were used!")

    print(f"\n=== Agent Made {len(tool_calls)} Tool Call(s) ===")

    # Extract and parse the structured response
    last_message = response["messages"][-1]

    try:
        # Parse the structured response using PydanticOutputParser
        structured_output = parser.parse(last_message.content)

        print("=== Successfully Parsed Structured Response ===")
        print(f"Topic: {structured_output.topic}")
        print(f"Summary: {structured_output.summary}")
        print(f"Sources: {structured_output.sources}")
        print(f"Tools used: {structured_output.tools_used}")

        print("\nTool calling agent with empty tools list worked successfully!")
        print("PydanticOutputParser successfully parsed the structured response!")

    except Exception as e:
        print(f"❌ Parsing error: {e}")
        print("Raw agent response:", last_message.content)


if __name__ == "__main__":
    main()
