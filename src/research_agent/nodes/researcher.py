from research_agent.state import ResearchState
from research_agent.tools.search import search


def researcher(state: ResearchState):
    plan = state["plan"]

    if plan is None:
        raise ValueError("Research plan is missing")

    sources = []

    for query in plan.search_queries:
        results = search(query)
        sources.extend(results)

    return {
        "sources": sources
    }