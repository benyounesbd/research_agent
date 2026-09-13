from research_agent.llm import client
from research_agent.schemas import Critique
from research_agent.state import ResearchState


def critic(state: ResearchState):
    question = state["question"]
    draft = state["draft"]
    sources = state["sources"]

    if draft is None:
        raise ValueError("Draft is missing")

    source_text = "\n\n".join(
        f"Title: {source.title}\n"
        f"URL: {source.url}\n"
        f"Content: {source.content}"
        for source in sources
    )

    critique = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_model=Critique,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research critic. "
                    "Evaluate whether the draft answers the question "
                    "and whether its claims are supported by the sources. "
                    "Approve the answer only if it is sufficiently accurate "
                    "and supported."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Draft: {draft}\n\n"
                    f"Sources: {source_text}"
                ),
            },
        ],
    )
    
    print("Critique:", critique)

    return {
        "critique": critique
    }