from research_agent.llm import client
from research_agent.state import ResearchState


def synthesizer(state: ResearchState):
    question = state["question"]
    plan = state["plan"]
    sources = state["sources"]

    if plan is None:
        raise ValueError("Research plan is missing")

    if not sources:
        raise ValueError("No sources found")

    draft = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_model=str,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research synthesizer. "
                    "Use the provided sources to create a coherent draft "
                    "that answers the user's question."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Plan: {plan}\n\n"
                    f"Sources: {sources}"
                ),
            },
        ],
    )

    print("Generated draft:", draft)

    return {
        "draft": draft
    }