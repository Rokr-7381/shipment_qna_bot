# Shipment QnA Bot — Architecture

## Goal
Provide a production-ready Shipment Q&A chatbot over a BYOD JSONL dataset using:
- FastAPI backend
- Streamlit demo UI
- LangGraph orchestration (Corrective/Reflective RAG later)
- Azure AI Search hybrid retrieval (BM25 + Vector)
- Azure OpenAI embeddings + chat (chat later)
- Strict consignee-scoped RLS (parent can see children; children cannot see siblings)

---

## High-level Components

### 1) API Layer (FastAPI)
Responsible for:
- request validation (Pydantic)
- trace_id + logging context initialization
- resolving effective consignee scope (RLS)
- hydrating conversation memory
- invoking compiled LangGraph workflow
- returning a structured response (answer + citations + optional table/chart spec)

**Non-goals**:
- no business logic in the route handler
- no RLS logic inside endpoints beyond calling the security/scope resolver

### 2) Orchestration Layer (LangGraph)
Nodes implement a deterministic pipeline:
- memory_in: load window + sticky slots into state
- normalizer: normalize question
- extractor: extract identifiers (container/po/obl/booking) and time windows
- intent: classify intent (primary) and optionally sub-intents (later)
- router: chooses execution path (retrieval handlers vs analytics)
- planner: builds retrieval plan (query_text/top_k/vector_k/extra_filter)
- retrieve: calls Azure AI Search tool w/ RLS filter (always)
- handlers: deterministic structured logic per intent (status/eta/delay/route/co2)
- judge/refine: corrective/reflective loop (later; only after deterministic handlers work)
- memory_out: store window + sticky slots
- formatter: final response formatting + citations + notices

### 3) Tool Layer
- azure_openai_embeddings: embed query
- azure_ai_search: hybrid search, RLS enforced
- analytics tools (optional): plan -> compile -> execute via pandas/sql
- sql tools (optional): SQLAlchemy engine + safe executor

### 4) Security Layer (RLS)
- scope resolver: validates parent/child relationship to produce allowed scope list
- rls filter builder: builds Azure Search filter string strictly from allowed scope
- all tools MUST accept `allowed_consignee_codes` and apply filter

### 5) Memory Layer
Stores per-conversation context:
- last 6–8 turns (window)
- sticky slots (recent container/po/obl/booking)
- last intent/time_window_days
No shipment facts are stored as truth—facts must be re-grounded via retrieval.

---

## Data Flow (Request → Response)

1) Client calls `POST /api/chat` with:
   - question: string
   - consignee_codes: string OR list (payload may contain comma-separated single string)
   - conversation_id: optional string; server generates if missing

2) Middleware:
   - sets `trace_id`
   - resolves `allowed_consignee_codes` using security/scope rules
   - sets log context (trace/conv/consignees)

3) Graph execution:
   - memory_in (hydrate)
   - normalizer (lowercase, normalize punctuation)
   - extractor (IDs + time window defaulting)
   - intent classifier
   - router:
     - Retrieval Path for structured intents (status/eta/delay/route/co2)
     - Analytics Path for chart/table queries
   - planner → retrieve
   - deterministic handler (if intent supported)
   - formatter (answer + citations + notices + optional chart/table spec)
   - memory_out (persist)

4) API returns `ChatResponse`.

---

## Mermaid Diagrams

### A) Runtime Call Flow
```mermaid
flowchart LR
  subgraph API[FastAPI Backend]
    R[POST /api/chat] --> MW[Middleware: trace_id + scope]
    MW --> H[Chat Handler: build GraphState]
  end

  subgraph LG[LangGraph Workflow]
    MIn[memory_in] --> N1[QueryNormalizer]
    N1 --> N2[Extractor]
    N2 --> N3[IntentClassifier]
    N3 --> RT[Router]
    RT -->|retrieval| PL[Planner]
    PL --> RE[Retriever]
    RE --> HD[Deterministic Handler]
    HD --> FM[Formatter]
    RT -->|analytics| AN[Analytics Node]
    AN --> FM
    FM --> MOut[memory_out]
  end

  H --> MIn
  MOut --> OUT[API Response]

