from typing import TypedDict

from research_agent.schemas import ResearchPlan, Source


class ResearchState(TypedDict):
    question: str
    plan: ResearchPlan | None
    sources: list[Source]
    draft: str | None