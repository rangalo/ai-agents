from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import time
import traceback

load_dotenv()

def test_wiki_tool():
    print("=== Testing Wikipedia Tool Root Cause ===\n")
    
    # Test 1: Basic WikipediaAPIWrapper
    print("1. Testing WikipediaAPIWrapper directly...")
    try:
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, max_summary_chars=100)
        print("✅ WikipediaAPIWrapper created successfully")
        
        # Test a simple query
        print("   Testing direct wrapper query...")
        start_time = time.time()
        result = api_wrapper.run("Paris")
        end_time = time.time()
        print(f"✅ Direct query completed in {end_time - start_time:.2f} seconds")
        print(f"   Result length: {len(result)} characters")
        print(f"   First 100 chars: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ WikipediaAPIWrapper failed: {e}")
        traceback.print_exc()
        return
    
    print()
    
    # Test 2: WikipediaQueryRun tool
    print("2. Testing WikipediaQueryRun tool...")
    try:
        wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        print("✅ WikipediaQueryRun created successfully")
        
        # Test tool execution
        print("   Testing tool.run()...")
        start_time = time.time()
        result = wiki_tool.run("Paris")
        end_time = time.time()
        print(f"✅ Tool query completed in {end_time - start_time:.2f} seconds")
        print(f"   Result: {result[:100]}...")
        
    except Exception as e:
        print(f"❌ WikipediaQueryRun failed: {e}")
        traceback.print_exc()
        return
    
    print()
    
    # Test 3: Different configurations that might cause issues
    print("3. Testing problematic configurations...")
    
    # Test with larger limits (might cause timeout)
    try:
        print("   Testing with larger limits...")
        large_wrapper = WikipediaAPIWrapper(top_k_results=5, max_summary_chars=1000)
        large_tool = WikipediaQueryRun(api_wrapper=large_wrapper)
        
        start_time = time.time()
        result = large_tool.run("Artificial Intelligence")
        end_time = time.time()
        print(f"✅ Large limits test completed in {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Large limits test failed: {e}")
    
    print()
    
    # Test 4: Test with complex queries that might cause issues
    print("4. Testing complex/problematic queries...")
    
    problematic_queries = [
        "What is the population of Tokyo?",  # This was in our original test
        "Latest AI developments",  # Non-encyclopedic query
        "Current weather",  # Real-time query (not suitable for Wikipedia)
        "NonExistentPageThatDoesNotExist12345",  # Non-existent page
        "",  # Empty query
    ]
    
    for query in problematic_queries:
        try:
            print(f"   Testing query: '{query}'")
            start_time = time.time()
            result = wiki_tool.run(query)
            end_time = time.time()
            print(f"   ✅ Completed in {end_time - start_time:.2f}s: {result[:50]}...")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print("\n=== Wiki Tool Analysis Complete ===")

if __name__ == "__main__":
    test_wiki_tool()