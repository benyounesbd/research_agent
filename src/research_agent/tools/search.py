from research_agent.schemas import Source
from tavily import TavilyClient

client = TavilyClient()

def search(query: str) -> list[Source]:
    response = client.search(query)
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