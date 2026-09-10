import sqlite3

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from research_agent.nodes.critic import critic
from research_agent.nodes.synthesizer import synthesizer
from research_agent.nodes.planner import planner
from research_agent.nodes.researcher import researcher
from research_agent.state import ResearchState

from research_agent.config import settings

def route_after_critic(state: ResearchState):
    critique = state["critique"]

    if critique is None:
        raise ValueError("Critique is missing")

    if critique.approved:
        return "end"

    if state["retry_count"] < settings.max_retries:
        return "research"
    
    return "end"

builder = StateGraph(ResearchState)

builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("synthesizer", synthesizer)
builder.add_node("critic", critic)

builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "synthesizer")
builder.add_edge("synthesizer", "critic")
builder.add_edge("critic", END)

builder.add_conditional_edges(
    "critic",
    route_after_critic,
    {
        "end": END,
        "research": "researcher",
    },
)

conn = sqlite3.connect(
    "research_agent.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(conn)

graph = builder.compile(checkpointer=checkpointer)

