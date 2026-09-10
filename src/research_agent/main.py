from fastapi import FastAPI, HTTPException

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
            "thread_id": request.thread_id
        }
    }
    try:
        result = graph.invoke(
            initial_state,
            config=config,
        )
    except Exception as exc:
        print(f"Research workflow failed: {exc}")
        raise HTTPException(status_code=500, detail="Research workflow failed")
    
    return {
        "draft": result["draft"],
        "critique": result["critique"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/research/{thread_id}")
def get_research(thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    snapshot = graph.get_state(config)

    return snapshot.values