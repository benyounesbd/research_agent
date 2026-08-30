from research_agent.graph import graph


def main():
    initial_state = {
        "question": "What is LangGraph?",
        "plan": None,
        "sources": [],
        "draft": None,
        "critique": None,
        "retry_count": 0,
    }

    result = graph.invoke(initial_state)
    print("\nFinal state:")
    print(result)
    


if __name__ == "__main__":
    main()