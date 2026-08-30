from research_agent.state import ResearchState
from research_agent.tools.search import search

MAX_SOURCES = 3

def researcher(state: ResearchState):
    plan = state["plan"]

    if plan is None:
        raise ValueError("Research plan is missing")

    sources = []
    seen_urls = set()

    for query in plan.search_queries:
        results = search(query)

        for source in results:
            if source.url in seen_urls:
                continue

            seen_urls.add(source.url)
            sources.append(source)

            if len(sources) >= MAX_SOURCES:
                break

        if len(sources) >= MAX_SOURCES:
            break

    return {
        "sources": sources
    }