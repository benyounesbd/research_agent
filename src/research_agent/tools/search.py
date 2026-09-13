from langsmith import traceable
from tavily import TavilyClient

from research_agent.config import settings
from research_agent.schemas import Source


class SearchError(Exception):
    pass


def get_search_client():
    if not settings.tavily_api_key:
        raise RuntimeError("TAVILY_API_KEY is not configured")

    return TavilyClient(api_key=settings.tavily_api_key)


@traceable(name="web_search")
def search(query: str) -> list[Source]:
    client = get_search_client()

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