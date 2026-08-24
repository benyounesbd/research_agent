from langgraph.graph import END, START, StateGraph

from research_agent.nodes.planner import planner
from research_agent.nodes.researcher import researcher
from research_agent.state import ResearchState

builder = StateGraph(ResearchState)

builder.add_node("planner", planner)
builder.add_node("researcher", researcher)


builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", END)

graph = builder.compile()
