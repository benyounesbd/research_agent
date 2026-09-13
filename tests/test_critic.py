from research_agent.nodes.critic import critic
from research_agent.schemas import Critique, Source


class FakeCompletions:
    def create(self, **kwargs):
        return Critique(
            approved=True,
            feedback="The answer is well supported by the sources.",
        )


class FakeChat:
    completions = FakeCompletions()


class FakeClient:
    chat = FakeChat()

def test_critic_approves_good_draft(monkeypatch):
    monkeypatch.setattr(
        "research_agent.nodes.critic.get_client",
        lambda: FakeClient(),
    )

    state = {
        "question": "What is LangGraph?",
        "plan": None,
        "sources": [
            Source(
                title="LangGraph Docs",
                url="https://example.com/langgraph",
                content="LangGraph is a framework for building agent workflows.",
            )
        ],
        "draft": "LangGraph is a framework for building agent workflows.",
        "critique": None,
        "retry_count": 1,
    }

    result = critic(state)

    assert result["critique"].approved is True
    assert (
        result["critique"].feedback
        == "The answer is well supported by the sources."
    )

class FakeCompletionsReject:
    def create(self, **kwargs):
        return Critique(
            approved=False,
            feedback="The answer needs more supporting evidence.",
        )


class FakeChatReject:
    completions = FakeCompletionsReject()


class FakeClientReject:
    chat = FakeChatReject()

def test_critic_rejects_weak_draft(monkeypatch):
    monkeypatch.setattr(
        "research_agent.nodes.critic.get_client",
        lambda: FakeClientReject(),
    )

    state = {
        "question": "What is LangGraph?",
        "plan": None,
        "sources": [
            Source(
                title="LangGraph Docs",
                url="https://example.com/langgraph",
                content="LangGraph is a framework for building agent workflows.",
            )
        ],
        "draft": "LangGraph is a programming language.",
        "critique": None,
        "retry_count": 1,
    }

    result = critic(state)

    assert result["critique"].approved is False
    assert "supporting evidence" in result["critique"].feedback