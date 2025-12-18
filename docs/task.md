# Task Checklist

- [x] **Phase 0: Observability (Priority)**
    - [x] Implement `logging/logger.py` (Structured Logging) <!-- id: 16 -->
    - [x] Implement `logging/middleware.py` (Context Management) <!-- id: 17 -->
    - [x] Implement `logging/graph_tracing.py` (Graph Callbacks) <!-- id: 18 -->

- [x] **Phase 1: Foundation & Security**
    - [x] Initialize project structure (folders, `__init__.py` files)
    - [x] Implement `security/scope.py` (Parent/Child logic) <!-- id: 0 -->
    - [x] Implement `security/rls.py` (Azure Filter Builder) <!-- id: 1 -->
    - [x] Verify RLS logic with unit tests <!-- id: 2 -->

- [x] **Phase 2: Core Graph & State**
    - [x] Define `graph/state.py` (GraphState) <!-- id: 3 -->
    - [x] Implement `graph/builder.py` with `MemorySaver` (In-Memory) <!-- id: 4 -->
    - [x] Implement `graph/nodes/normalizer.py` & `extractor.py` <!-- id: 5 -->
    - [x] Implement `graph/nodes/intent.py` & `router.py` <!-- id: 6 -->

- [x] **Phase 3: Retrieval & Tools**
    - [x] Implement `tools/azure_ai_search.py` (Hybrid Search + RLS) <!-- id: 7 -->
    - [x] Implement `graph/nodes/planner.py` & `retrieve.py` <!-- id: 8 -->
    - [x] Implement `graph/nodes/handlers/` (Status, ETA, Delay) <!-- id: 9 -->

- [x] **Phase 4: API & Integration**
    - [x] Implement `api/routes/chat.py` (Endpoint) <!-- id: 10 -->
    - [x] Implement `api/main.py` (App entrypoint) <!-- id: 11 -->
    - [x] Connect Basic Web UI (`static/index.html`) <!-- id: 12 -->

- [/] **Phase 5: Verification & Refinement**
    - [x] Fix 404 and Logging issues <!-- id: 13.1 -->
    - [ ] Run end-to-end tests <!-- id: 13 -->
    - [ ] Address "Time Travel" data gap (Design decision needed) <!-- id: 14 -->
    - [ ] Address "Durable Execution" (Switch to Checkpointer?) <!-- id: 15 -->
