from research_agent.schemas import Source


def search(query: str) -> list[Source]:
    return [
        Source(
            title=f"Result for {query}",
            url="https://example.com",
            content=f"Fake search result for: {query}",
        )
    ]