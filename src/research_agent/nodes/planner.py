from research_agent.state import ResearchState


def planner(state: ResearchState):
    print("Question:", state["question"])

    return {
        "plan": {
            "sub_questions": ["What is LangGraph?"],
            "search_queries": ["LangGraph tutorial"],
        }
    }