# Research Agent

> Un agente autónomo que planifica, investiga, sintetiza y **se autoevalúa** con un bucle de reintentos.
> An autonomous agent that plans, researches, synthesizes and **self-critiques** with a retry loop.

[EN](#en) · [ES](#es)

---

## EN

### What it does

Feed it a question and the system:

1. **Plans** the research into sub-questions and search queries.
2. **Researches** with Tavily (real web search), deduplicating sources.
3. **Synthesizes** an answer grounded in the sources.
4. **Critiques** its own answer: does it answer the question? Is it supported by the sources?
5. If it fails the critique, it **retries** (up to 2 times) re-researching and re-synthesizing.

```
   Question
      ↓
   Planner ──────────────► ResearchPlan (Pydantic)
      ↓
   Researcher ───────────► Tavily (web search) → list[Source]
      ↓
   Synthesizer ──────────► str draft
      ↓
   Critic ───────────────► Critique {approved, feedback}
      ↓
   approved?  ───────────► no ──► Researcher (loop, max 2)
      ↓ yes
     END
```

Graph flow: `planner → researcher → synthesizer → critic` with a **conditional edge** routing back to `researcher` when the answer is not approved.

### Why this project

Built from scratch and tested end-to-end, this project demonstrates the core skills of an **AI Engineer**:

- **LangGraph**: stateful agent workflows — state, nodes, edges, `StateGraph`, conditional edges and loops.
- **Instructor**: guaranteed structured LLM output through Pydantic.
- **Pydantic**: validated schemas (`ResearchPlan`, `Source`, `Critique`).
- **Layered design**: nodes only know the State contract; `tools/search.py` isolates the search provider (Tavily), so it can be swapped without touching the pipeline.
- **Model-agnostic**: uses Gemini through the OpenAI-compatible endpoint of the `openai` client, so you can point to any compatible provider (OpenAI, Groq, Ollama, OpenRouter) in 3 lines.

### Stack

```
Python ≥ 3.12
├── LangGraph   → orchestration / state / flow
├── Instructor  → structured LLM outputs
├── Pydantic    → schemas / validation
├── OpenAI SDK  → client (pointing to Gemini)
├── Tavily      → real web search
└── pytest      → tests (roadmap)
```

### Run it

```bash
uv sync
uv run python -m research_agent.main
```

You need a root-level `.env`:

```env
GEMINI_API_KEY=...
TAVILY_API_KEY=...
```

Environment managed with `uv` (package manager + venv + lockfile in one tool).

### Structure

```
src/research_agent/
├── __init__.py
├── main.py            # entrypoint: invokes the graph
├── graph.py           # StateGraph + conditional edges + retries
├── llm.py             # Instructor client (Gemini via OpenAI)
├── state.py           # ResearchState (TypedDict)
├── schemas.py         # ResearchPlan, Source, Critique (Pydantic)
├── nodes/
│   ├── planner.py
│   ├── researcher.py
│   ├── synthesizer.py
│   └── critic.py
└── tools/
    └── search.py      # Tavily CLI, isolated from the workflow
```

### Practices implemented

- `TypedDict` describes the State; Pydantic does runtime validation on the object itself.
- A node reads the State and returns **only** the fields it updates.
- URL deduplication in the researcher.
- Retry cap (`MAX_RETRIES`) to avoid infinite loops.
- Secrets in `.env`, out of the repo (`.gitignore`).

### Roadmap

- [ ] pytest (graph and node tests)
- [ ] LangSmith (tracing / evaluation)
- [ ] OpenTelemetry (observability)
- [ ] State persistence (checkpoints)
- [ ] FastAPI (expose the agent as an API)

---

## ES

### ¿Qué hace?

Le das una pregunta y el sistema:

1. **Planifica** la investigación en sub-preguntas y queries de búsqueda.
2. **Investiga** usando Tavily (búsqueda web real), con deduplicación de fuentes.
3. **Sintetiza** una respuesta a partir de las fuentes.
4. **Crítica** su propia respuesta: ¿responde a la pregunta? ¿está respaldada por las fuentes?
5. Si no aprueba, **reintenta** (hasta 2 veces) re-investigando y re-sintetizando.

```
   Pregunta
      ↓
   Planner ──────────────► ResearchPlan (Pydantic)
      ↓
   Researcher ───────────► Tavily (web search) → list[Source]
      ↓
   Synthesizer ──────────► str draft
      ↓
   Critic ───────────────► Critique {approved, feedback}
      ↓
   ¿approved?  ─────────► no ──► Researcher (bucle, máx. 2)
      ↓ sí
     END
```

Flujo del grafo: `planner → researcher → synthesizer → critic` con un **conditional edge** que rutea de vuelta a `researcher` cuando la respuesta no aprueba.

### Por qué este proyecto

Construido de cero y probado de punta a punta, este proyecto demuestra las habilidades centrales de un **AI Engineer**:

- **LangGraph**: stateful workflows de agentes — state, nodes, edges, `StateGraph`, conditional edges y loops.
- **Instructor**: salida estructurada garantizada del LLM a través de Pydantic.
- **Pydantic**: schemas con validación (`ResearchPlan`, `Source`, `Critique`).
- **Design por niveles**: los nodes conocen el contrato del State; `tools/search.py` aísla al proveedor de búsqueda (Tavily), así que se puede cambiar sin tocar el pipeline.
- **Modelo-agnóstico**: usa Gemini vía el endpoint compatible con OpenAI del cliente `openai`, así que se puede apuntar a cualquier proveedor compatible (OpenAI, Groq, Ollama, OpenRouter) con 3 líneas.

### Stack

```
Python ≥ 3.12
├── LangGraph   → orquestación / state / flujo
├── Instructor  → salidas LLM estructuradas
├── Pydantic    → schemas / validación
├── OpenAI SDK  → cliente (apuntando a Gemini)
├── Tavily      → búsqueda web real
└── pytest      → tests (roadmap)
```

### Cómo ejecutar

```bash
uv sync
uv run python -m research_agent.main
```

Necesitas un `.env` en la raíz:

```env
GEMINI_API_KEY=...
TAVILY_API_KEY=...
```

Ambientación con `uv` (package manager + venv + lockfile en un solo tool).

### Estructura

```
src/research_agent/
├── __init__.py
├── main.py            # entrypoint: invoke el grafo
├── graph.py           # StateGraph + conditional edges + retries
├── llm.py             # cliente Instructor (Gemini vía OpenAI)
├── state.py           # ResearchState (TypedDict)
├── schemas.py         # ResearchPlan, Source, Critique (Pydantic)
├── nodes/
│   ├── planner.py
│   ├── researcher.py
│   ├── synthesizer.py
│   └── critic.py
└── tools/
    └── search.py      # CLI de Tavily, aislado del workflow
```

### Buenas prácticas implementadas

- `TypedDict` describe el State; Pydantic hace validación runtime en el propio objeto.
- Un node lee el State y devuelve **solo** los campos que actualiza.
- Deduplicación de URLs en el investigador.
- Freno de reintentos (`MAX_RETRIES`) para evitar loops infinitos.
- Secretos en `.env`, fuera del repo (`.gitignore`).

### Roadmap

- [ ] pytest (tests del grafo y nodes)
- [ ] LangSmith (tracing / evaluación)
- [ ] OpenTelemetry (observabilidad)
- [ ] Persistencia del State (checkpoints)
- [ ] FastAPI (exponer el agente como API)

---

## License

MIT