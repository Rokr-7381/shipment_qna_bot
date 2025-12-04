# Implementation Plan - Shipment QnA Bot

## Goal Description
Build a production-ready Shipment Q&A bot with strict RLS, hybrid retrieval, and deterministic answers.

## User Review Required
> [!IMPORTANT]
> **Durable Execution Strategy**: Per your request (Session only, no DB, no cost), we will use **`MemorySaver`**. This stores state in **RAM**.
> *   **Pros:** Zero setup, zero files, zero cost.
> *   **Cons:** If the server restarts, active conversations are lost.
> *   **Future-Proof:** Switching to Postgres later is a 1-line code change (replace `MemorySaver` with `PostgresSaver`).

> [!WARNING]
> **Data Model for Time Travel**: Answering "What was the ETA yesterday?" requires historical snapshots in the index or database. The current index schema only supports "Current State". We need to decide if we are building a history-aware index or just a current-state bot.

## Proposed Changes

### Logging Layer (Phase 0 - Priority)
#### [NEW] [logger.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/logging/logger.py)
- Configure `structlog` or standard logging with JSON output.
- Ensure `trace_id` and `conversation_id` are included in every log.

#### [NEW] [middleware.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/logging/middleware.py)
- FastAPI middleware to initialize `trace_id` and ContextVars.

#### [NEW] [graph_tracing.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/logging/graph_tracing.py)
- LangChain/LangGraph callbacks to log node transitions and state updates.

### Security Layer
#### [NEW] [scope.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/security/scope.py)
- `resolve_allowed_scope(user, payload)`: Enforces Parent > Child hierarchy.

#### [NEW] [rls.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/security/rls.py)
- `build_search_filter(allowed_codes)`: Generates OData filter for Azure Search.

### Graph Layer
#### [NEW] [state.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/graph/state.py)
- Define `GraphState` TypedDict.

#### [NEW] [builder.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/graph/builder.py)
- Construct the LangGraph workflow.
- **Use `MemorySaver`** (In-Memory Checkpointer).

### Tools Layer
#### [NEW] [azure_ai_search.py](file:///c:/Users/CHOWDHURYRaju/Desktop/shipment_qna_bot/src/shipment_qna_bot/tools/azure_ai_search.py)
- `search(query, allowed_codes)`: Executes hybrid search with mandatory filter.

## Verification Plan

### Automated Tests
- Unit tests for `scope.py` to verify parent/child logic.
- Unit tests for `rls.py` to verify filter string generation.
- Mocked graph tests to verify routing logic.

### Manual Verification
- Use `verify_fix.py` (or similar script) to simulate API calls with different user scopes and verify data leakage does not occur.
