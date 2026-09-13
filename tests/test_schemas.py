import pytest
from pydantic import ValidationError

from research_agent.schemas import ResearchPlan


def test_research_plan_is_valid():
    plan = ResearchPlan(
        sub_questions=["What is LangGraph?"],
        search_queries=["LangGraph overview"],
    )

    assert plan.sub_questions == ["What is LangGraph?"]
    assert plan.search_queries == ["LangGraph overview"]


def test_research_plan_requires_sub_questions():
    with pytest.raises(ValidationError):
        ResearchPlan(
            sub_questions=[],
            search_queries=["LangGraph overview"],
        )
