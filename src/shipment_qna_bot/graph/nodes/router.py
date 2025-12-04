from typing import Literal

from shipment_qna_bot.graph.state import GraphState
from shipment_qna_bot.logging.logger import logger


def route_node(state: GraphState) -> Literal["retrieval", "analytics", "end"]:
    """
    Decides the next path based on intent.
    """
    intent = state.get("primary_intent")

    if intent == "analytics":
        return "analytics"
    elif intent in ["eta", "status", "delay"]:
        return "retrieval"
    else:
        return "end"
