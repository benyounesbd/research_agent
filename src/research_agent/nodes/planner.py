from research_agent.config import settings
from research_agent.llm import get_client
from research_agent.schemas import ResearchPlan
from research_agent.state import ResearchState


def planner(state: ResearchState):
    question = state["question"]

    client = get_client()
    plan = client.chat.completions.create(
        model=settings.llm_model,
        response_model=ResearchPlan,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research planner. "
                    "Break the user's question into useful "
                    "sub-questions and search queries."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    print("Generated plan:", plan)

    return {
        "plan": plan
}