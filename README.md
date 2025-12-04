# Shipment QnA Bot

A production-ready Shipment Q&A chatbot using **LangGraph**, **Azure AI Search**, and **FastAPI**.

## Key Features
*   **LangGraph Orchestration**: Deterministic workflows with "Time Travel" debugging capabilities.
*   **Strict RLS**: Row-Level Security enforced at the application level (Parent sees Children, Child sees only self).
*   **Hybrid Retrieval**: Azure AI Search (BM25 + Vector) with mandatory RLS filters.
*   **Durable Execution**: Uses `MemorySaver` (In-Memory) for session continuity, ready for Postgres.
*   **Observability**: Structured JSON logging with `trace_id` and graph execution tracing.

---

## Folder Structure

```text
shipment_qna_bot/
├─ docs/                 # Documentation & Plans
│  ├─ architecture.md
│  ├─ rls_model.md
│  ├─ index_schema.md
│  ├─ task.md            # Progress Checklist
│  └─ implementation_plan.md
├─ src/
│  └─ shipment_qna_bot/
│     ├─ logging/        # Observability (Logger, Middleware, Tracing)
│     ├─ security/       # RLS & Scope Resolution
│     ├─ graph/          # LangGraph Workflow (State, Nodes, Builder)
│     ├─ tools/          # Azure Search, OpenAI, SQL tools
│     ├─ api/            # FastAPI Routes
│     └─ ui/             # Streamlit Demo
└─ tests/                # Unit & Integration Tests
```

---

## Progress
- [x] **Phase 0: Observability**: Structured logging and graph tracing implemented.
- [x] **Phase 1: Security**: RLS scope resolution and filter building implemented & verified.
- [ ] **Phase 2: Core Graph**: Implementing State, Nodes, and Workflow.
- [ ] **Phase 3: Retrieval**: Connecting to Azure AI Search.
- [ ] **Phase 4: API**: Exposing endpoints.

---

## Getting Started
1.  **Install dependencies**: `pip install -r requirements.txt`
2.  **Run Tests**: `pytest`
3.  **Run App**: `uvicorn shipment_qna_bot.api.main:app --reload` (Coming soon)



---
