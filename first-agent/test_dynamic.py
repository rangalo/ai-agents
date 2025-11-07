from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import search_tool, wiki_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

def test_dynamic_query(query):    
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        parser = PydanticOutputParser(pydantic_object=ResearchResponse)
        tools = [search_tool, wiki_tool]

        agent = create_agent(
            model=llm,
            system_prompt=f"""You are a research assistant. 
            
            CRITICAL: You MUST use the available tools to gather information before responding. 
            ALWAYS start by using the search tool to find current, accurate information.
            
            Available tools:
            - search: For current web information  
            - wiki: For encyclopedic information
            
            Process:
            1. FIRST: Use the search tool to find current information
            2. OPTIONALLY: Use wiki tool for additional information
            3. Provide response in JSON format: {parser.get_format_instructions()}
            
            You MUST use tools - do not provide responses without using tools first.""",
            tools=tools
        )

        print(f"🔍 Testing query: '{query}'")
        print("📡 Invoking agent...")

        response = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        # Check for tool usage
        tool_calls = []
        for message in response["messages"]:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_calls.append(f"🔍 Used {tool_call['name']} with: {tool_call['args']}")
        
        print(f"\n=== Tool Usage Analysis ===")
        print(f"Number of tool calls: {len(tool_calls)}")
        
        if tool_calls:
            print("✅ Tools were used:")
            for call in tool_calls:
                print(f"  {call}")
        else:
            print("❌ NO TOOLS WERE USED!")
            print("This indicates the agent is not following instructions to use tools.")
            
        # Show the final response
        last_message = response["messages"][-1]
        print(f"\n=== Final Response ===")
        print(f"Content: {last_message.content[:200]}...")
        
        return len(tool_calls) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Test with different types of queries
    test_queries = [
        "What is the population of Tokyo?",
        "Tell me about climate change",
        "What are the latest AI developments?",
        "Explain quantum computing"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"TEST {i}: {query}")
        print('='*50)
        used_tools = test_dynamic_query(query)
        print(f"Result: {'✅ TOOLS USED' if used_tools else '❌ NO TOOLS USED'}")
        if i < len(test_queries):
            print("\nWaiting before next test...")