from shipment_qna_bot.graph.state import GraphState
from shipment_qna_bot.logging.logger import logger


def normalize_node(state: GraphState) -> GraphState:
    """
    Normalizes the user's question.
    """
    question = state.get("question", "").strip()
    normalized = question.lower()

    logger.info(
        f"Normalized question: {normalized}",
        extra={"extra_data": {"original": question}},
    )

    return {"normalized_question": normalized}
