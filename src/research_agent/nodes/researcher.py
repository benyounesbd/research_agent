from research_agent.state import ResearchState


def researcher(state: ResearchState):
    print("Research plan:", state["plan"])

    return {
        "sources": []
    }