from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
import time
import signal
import sys

load_dotenv()


def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")


def test_agent_with_wiki():
    print("=== Testing Agent + Wiki Tool Integration ===\n")

    # Create tools
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="search", func=search.run, description="Search the web for information"
    )

    api_wrapper = WikipediaAPIWrapper(top_k_results=1, max_summary_chars=100)
    wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Test scenarios
    test_cases = [
        {
            "name": "Agent with ONLY search tool",
            "tools": [search_tool],
            "query": "What is the population of Tokyo?",
        },
        {
            "name": "Agent with ONLY wiki tool",
            "tools": [wiki_tool],
            "query": "What is the population of Tokyo?",
        },
        {
            "name": "Agent with BOTH tools",
            "tools": [search_tool, wiki_tool],
            "query": "What is the population of Tokyo?",
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
        print("-" * 50)

        try:
            # Set up timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(30)  # 30 second timeout

            agent = create_agent(
                model=llm,
                system_prompt="You are a helpful assistant. Use available tools to answer questions.",
                tools=test_case["tools"],
            )

            print(f"   Query: {test_case['query']}")
            print("   Creating agent response...")

            start_time = time.time()
            response = agent.invoke(
                {"messages": [{"role": "user", "content": test_case["query"]}]}
            )
            end_time = time.time()

            # Cancel timeout
            signal.alarm(0)

            # Count tool calls
            tool_calls = []
            for message in response["messages"]:
                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_calls.append(tool_call["name"])

            print(f"   ✅ SUCCESS in {end_time - start_time:.2f} seconds")
            print(f"   Tools used: {tool_calls}")
            print(
                f"   Final response length: {len(response['messages'][-1].content)} chars"
            )

        except TimeoutError:
            print("   ❌ TIMEOUT - This configuration causes hangs!")
            signal.alarm(0)  # Cancel timeout

        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            signal.alarm(0)  # Cancel timeout

        print()

    print("=== Analysis Complete ===")


if __name__ == "__main__":
    test_agent_with_wiki()
