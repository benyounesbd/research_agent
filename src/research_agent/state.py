from typing import TypedDict

from research_agent.schemas import Critique, ResearchPlan, Source


class ResearchState(TypedDict):
    question: str
    plan: ResearchPlan | None
    sources: list[Source]
    draft: str | None
    critique: Critique | None
    retry_count: int