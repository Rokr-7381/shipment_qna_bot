# src/shipment_qna_bot/graph/nodes/planner.py

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from shipment_qna_bot.graph.state import RetrievalPlan
from shipment_qna_bot.logging.graph_tracing import log_node_execution
from shipment_qna_bot.logging.logger import logger, set_log_context


def _ids_only(pairs: List[Tuple[str, float]] | None) -> List[str]:
    if not pairs:
        return []
    return [p[0] for p in pairs if p and p[0]]


# find critix
def _sync_ctx(state: Dict[str, Any]) -> None:
    # set_log_context({"step": "NODE:Planner", "state": _summarize_state(state)})
    set_log_context(
        conversation_id=state.get("conversation_id", "-"),
        consignee_codes=state.get("consignee_codes", []),
        intent=state.get("intent", "-"),
    )


def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produces:
      state["retrieval_plan"] = {
        query_text, top_k, vector_k, extra_filter, reason
      }
    """
    _sync_ctx(state)

    with log_node_execution(
        "Planner",
        {
            "intent": state.get("intent", "-"),
            "normalized_question": (state.get("normalized_question") or "-")[:120],
            "time_window_days": state.get("time_window_days"),
        },
    ):
        intent = state.get("intent", "generic")
        q = (
            state.get("normalized_question") or state.get("question_raw") or ""
        ).strip()

        # Extract IDs from the dictionary populated by extractor_node
        extracted = state.get("extracted_ids") or {}
        containers = extracted.get("container") or []
        pos = extracted.get("po") or []
        obls = extracted.get("obl") or []
        bookings = extracted.get("booking") or []

        # Build query text: prioritize identifiers if present
        id_tokens = [*containers, *obls, *pos, *bookings]
        query_text = " ".join(id_tokens).strip() or q

        extra_filter = None
        plan: RetrievalPlan = {
            "query_text": query_text,
            "top_k": 5,
            "vector_k": 30,
            "extra_filter": extra_filter,
            "reason": f"intent={intent}; ids={bool(id_tokens)}",
        }

        state["retrieval_plan"] = plan

        logger.info(
            f"Planned retrieval: query_text='{query_text[:80]}' top_k={plan['top_k']} vector_k={plan['vector_k']} "
            f"extra_filter={'yes' if extra_filter else 'no'} reason={plan['reason']}",
            extra={"step": "NODE:Planner"},
        )

        return state
