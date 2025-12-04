from shipment_qna_bot.graph.state import GraphState
from shipment_qna_bot.logging.logger import logger


def intent_node(state: GraphState) -> GraphState:
    """
    Classifies the user's intent.
    For Phase 2, we use simple keyword matching. Phase 3 will use LLM.
    """
    text = state.get("normalized_question", "")

    intent = "unknown"

    if "chart" in text or "analytics" in text:
        intent = "analytics"
    elif "eta" in text or "arrive" in text:
        intent = "eta"
    elif "status" in text or "where" in text:
        intent = "status"
    elif "delay" in text:
        intent = "delay"

    logger.info(
        f"Classified intent: {intent}",
        extra={"extra_data": {"text_snippet": text[:50]}},
    )

    return {"primary_intent": intent}
