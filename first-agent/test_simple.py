from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


def test_agent_with_dynamic_query():
    # Create simple search tool
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="search",
        func=search.run,
        description="Search the web for information. Input should be a search query string.",
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    agent = create_agent(
        model=llm,
        system_prompt=f"""You are a helpful assistant. 
        
        IMPORTANT: For ANY user question, you MUST use the search tool first to find current information.
        
        Process:
        1. Use the search tool to find information
        2. Provide response in this JSON format: {parser.get_format_instructions()}
        
        NEVER provide a response without using the search tool first.""",
        tools=[search_tool],
    )

    # Test different types of queries
    test_queries = [
        "What is 2 + 2?",  # Simple math - agent might not use tools
        "What is the current population of Tokyo?",  # Should definitely use search
        "Tell me about recent AI developments",  # Should use search
        "What is the weather like today?",  # Should use search
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"TESTING: {query}")
        print("=" * 60)

        try:
            response = agent.invoke({"messages": [{"role": "user", "content": query}]})

            # Count tool usage
            tool_calls = []
            for message in response["messages"]:
                if hasattr(message, "tool_calls") and message.tool_calls:
                    tool_calls.extend(message.tool_calls)

            print(f"🔍 Tool calls made: {len(tool_calls)}")

            if tool_calls:
                print("✅ AGENT USED TOOLS:")
                for call in tool_calls:
                    print(f"  - {call['name']}: {call['args']}")
            else:
                print("❌ AGENT DID NOT USE TOOLS!")
                print(
                    "This suggests the agent is not following the instruction to always use search."
                )

            # Show final response
            final_message = response["messages"][-1]
            print(
                f"\n📄 Final response (first 100 chars): {final_message.content[:100]}..."
            )

        except Exception as e:
            print(f"❌ Error processing query: {e}")


if __name__ == "__main__":
    test_agent_with_dynamic_query()
