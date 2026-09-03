from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from research_agent.graph import graph
from research_agent.schemas import ResearchRequest

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

@app.post("/research")
def start_research(request: ResearchRequest):
    initial_state = {
        "question": request.question,
        "plan": None,
        "sources": [],
        "draft": None,
        "critique": None,
        "retry_count": 0,
    }

    config = {
        "configurable": {
            "thread_id": "research-123"
        }
    }

    result = graph.invoke(
        initial_state,
        config=config,
    )

    snapshot = graph.get_state(config)

    print("Estado persistido:")
    print(snapshot.values)

    return {
        "draft": result["draft"],
        "critique": result["critique"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}