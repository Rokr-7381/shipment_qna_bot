# Task Checklist

- [ ] **Phase 0: Observability (Priority)**
    - [ ] Implement `logging/logger.py` (Structured Logging) <!-- id: 16 -->
    - [ ] Implement `logging/middleware.py` (Context Management) <!-- id: 17 -->
    - [ ] Implement `logging/graph_tracing.py` (Graph Callbacks) <!-- id: 18 -->

- [ ] **Phase 1: Foundation & Security**
    - [ ] Initialize project structure (folders, `__init__.py` files)
    - [ ] Implement `security/scope.py` (Parent/Child logic) <!-- id: 0 -->
    - [ ] Implement `security/rls.py` (Azure Filter Builder) <!-- id: 1 -->
    - [ ] Verify RLS logic with unit tests <!-- id: 2 -->

- [ ] **Phase 2: Core Graph & State**
    - [ ] Define `graph/state.py` (GraphState) <!-- id: 3 -->
    - [ ] Implement `graph/builder.py` with `MemorySaver` (In-Memory) <!-- id: 4 -->
    - [ ] Implement `graph/nodes/normalizer.py` & `extractor.py` <!-- id: 5 -->
    - [ ] Implement `graph/nodes/intent.py` & `router.py` <!-- id: 6 -->

- [ ] **Phase 3: Retrieval & Tools**
    - [ ] Implement `tools/azure_ai_search.py` (Hybrid Search + RLS) <!-- id: 7 -->
    - [ ] Implement `graph/nodes/planner.py` & `retrieve.py` <!-- id: 8 -->
    - [ ] Implement `graph/nodes/handlers/` (Status, ETA, Delay) <!-- id: 9 -->

- [ ] **Phase 4: API & Integration**
    - [ ] Implement `api/routes/chat.py` (Endpoint) <!-- id: 10 -->
    - [ ] Implement `api/main.py` (App entrypoint) <!-- id: 11 -->
    - [ ] Connect Streamlit UI (`ui/streamlit_app.py`) <!-- id: 12 -->

- [ ] **Phase 5: Verification & Refinement**
    - [ ] Run end-to-end tests <!-- id: 13 -->
    - [ ] Address "Time Travel" data gap (Design decision needed) <!-- id: 14 -->
    - [ ] Address "Durable Execution" (Switch to Checkpointer?) <!-- id: 15 -->
