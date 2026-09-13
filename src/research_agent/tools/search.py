from langsmith import traceable
from tavily import TavilyClient

from research_agent.schemas import Source

client = TavilyClient()

class SearchError(Exception):
    pass

@traceable(name="web_search")
def search(query: str) -> list[Source]:
    try:
        response = client.search(query)
    except Exception as exc:
        raise SearchError("Web search failed") from exc

    return [
        Source(
            title=result["title"],
            url=result["url"],
            content=result["content"],
        )
        for result in response["results"]
    ]       

if __name__ == "__main__":
    results = search("What is LangGraph?")

    for result in results:
        print(result)