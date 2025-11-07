from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="""Search the web for current, accurate information about any topic. 
    Use this tool to find facts, statistics, recent news, and reliable sources.
    Input should be a clear search query about the topic you need information on.
    Returns relevant web search results with factual content.""",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, max_summary_chars=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


def save_to_file(data: str, filename: str = "research_output.txt"):
    """Saves the given data to a text file with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{timestamp}_{filename}"
    formatted_text = f"---- Research Output-----\n{data}\n-----------------------"
    with open(full_filename, "w") as file:
        file.write(formatted_text)
    return f"Successfully saved to {full_filename}"


save_tool = Tool(
    name="save_to_file",
    func=save_to_file,
    description="Saves the provided research data to a timestamped text file. Input should be the research output text.",
)
