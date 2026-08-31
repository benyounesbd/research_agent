from research_agent.nodes.researcher import researcher
from research_agent.schemas import ResearchPlan, Source

import pytest

def test_researcher_collects_sources(monkeypatch):
    def fake_search(query: str):
        return [
            Source(
                title="LangGraph Docs",
                url="https://example.com/langgraph",
                content="LangGraph is a framework for building agent workflows.",
            ),
            Source(
                title="LangGraph Guide",
                url="https://example.com/guide",
                content="LangGraph provides graph-based orchestration.",
            ),
        ]

    monkeypatch.setattr(
        "research_agent.nodes.researcher.search",
        fake_search,
    )

    plan = ResearchPlan(
        sub_questions=["What is LangGraph?"],
        search_queries=["LangGraph"],
    )

    state = {
        "question": "What is LangGraph?",
        "plan": plan,
        "sources": [],
        "draft": None,
        "critique": None,
        "retry_count": 0,
    }

    result = researcher(state)

    assert len(result["sources"]) == 2
    assert result["sources"][0].title == "LangGraph Docs"
    assert result["retry_count"] == 1


def test_researcher_removes_duplicate_sources(monkeypatch):
    def fake_search(query: str):
        return [
            Source(
                title="LangGraph Docs",
                url="https://example.com/langgraph",
                content="LangGraph is a framework.",
            ),
            Source(
                title="LangGraph Guide",
                url="https://example.com/guide",
                content="A guide to LangGraph.",
            ),
        ]

    monkeypatch.setattr(
        "research_agent.nodes.researcher.search",
        fake_search,
    )

    plan = ResearchPlan(
        sub_questions=[
            "What is LangGraph?",
            "What does LangGraph do?",
        ],
        search_queries=[
            "LangGraph",
            "LangGraph purpose",
        ],
    )

    state = {
        "question": "What is LangGraph?",
        "plan": plan,
        "sources": [],
        "draft": None,
        "critique": None,
        "retry_count": 0,
    }

    result = researcher(state)

    urls = [source.url for source in result["sources"]]

    assert len(urls) == len(set(urls))
    assert len(result["sources"]) == 2

def test_researcher_requires_plan():
    state = {
        "question": "What is LangGraph?",
        "plan": None,
        "sources": [],
        "draft": None,
        "critique": None,
        "retry_count": 0,
    }

    with pytest.raises(ValueError, match="Research plan is missing"):
        researcher(state)