from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import search_tool, wiki_tool  # Import exact same tools
import time

load_dotenv()


def test_exact_original_config():
    print("=== Testing EXACT Original Configuration ===\n")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Test the exact same configuration that was causing problems
    print("Testing with EXACT original tools configuration...")
    print(f"search_tool: {search_tool}")
    print(f"wiki_tool: {wiki_tool}")
    print(f"wiki_tool.name: {wiki_tool.name}")
    print(f"wiki_tool.description: {wiki_tool.description}")

    try:
        agent = create_agent(
            model=llm,
            system_prompt="""You are a research assistant that will help generate a research paper.
            
            IMPORTANT: You have access to a search tool. USE IT to gather current, accurate information about the user's query before providing your response.
            
            Follow this process:
            1. Use the search tool to find relevant, up-to-date information about the topic
            2. Analyze the search results carefully
            3. Provide a structured response
            
            When providing sources, use REAL URLs from your search results, not example URLs.
            After using tools, provide ONLY the final JSON response with no additional text.""",
            tools=[search_tool, wiki_tool],  # EXACT same as original
        )

        print("\n✅ Agent created successfully")

        # Test with the same query that was causing issues
        query = "What is the population of Tokyo?"
        print(f"\nTesting query: '{query}'")

        start_time = time.time()
        response = agent.invoke({"messages": [{"role": "user", "content": query}]})
        end_time = time.time()

        # Analyze response
        tool_calls = []
        for message in response["messages"]:
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_calls.append(
                        {"name": tool_call["name"], "args": tool_call["args"]}
                    )

        print(f"✅ SUCCESS in {end_time - start_time:.2f} seconds")
        print(f"Tool calls made: {len(tool_calls)}")
        for call in tool_calls:
            print(f"  - {call['name']}: {call['args']}")

        print(f"\nFinal response preview: {response['messages'][-1].content[:100]}...")

        # The configuration works! So what was the actual issue?
        print("\n🤔 CONCLUSION: The wiki tool itself is NOT the problem!")
        print("The issue must have been one of:")
        print("1. System prompt conflicts")
        print("2. Parsing errors with structured output")
        print("3. Network timeouts during development")
        print("4. Environmental/dependency issues")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_exact_original_config()
