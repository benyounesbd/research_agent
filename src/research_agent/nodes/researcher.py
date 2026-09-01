from research_agent.state import ResearchState
from research_agent.tools.search import search
from research_agent.observability import tracer

MAX_SOURCES = 3

def researcher(state: ResearchState):
    plan = state["plan"]

    if plan is None:
        raise ValueError("Research plan is missing")

    with tracer.start_as_current_span("researcher") as span:
        span.set_attribute(
        "research.query_count",
            len(plan.search_queries),
        )

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

        span.set_attribute(
            "research.source_count",
            len(sources),
        )

        return {
            "sources": sources,
            "retry_count": state["retry_count"] + 1,
        }