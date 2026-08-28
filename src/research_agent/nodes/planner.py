from research_agent.state import ResearchState
from research_agent.llm import client
from research_agent.schemas import ResearchPlan

def planner(state: ResearchState):
    question = state["question"]

    plan = client.chat.completions.create(
        model="gemini-2.5-flash",
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