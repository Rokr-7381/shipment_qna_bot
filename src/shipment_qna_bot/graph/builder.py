from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from shipment_qna_bot.graph.nodes.extractor import extractor_node
from shipment_qna_bot.graph.nodes.intent import intent_node
from shipment_qna_bot.graph.nodes.normalizer import normalize_node
from shipment_qna_bot.graph.nodes.router import route_node
from shipment_qna_bot.graph.state import GraphState


def build_graph():
    """
    Constructs the shipment QnA graph.
    """
    workflow = StateGraph(GraphState)

    # --- Add Nodes ---
    workflow.add_node("normalizer", normalize_node)
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("intent", intent_node)
    # workflow.add_node("planner", planner_node) # Coming in Phase 3
    # workflow.add_node("retrieve", retrieve_node) # Coming in Phase 3

    # --- Add Edges ---
    # Start -> Normalizer
    workflow.set_entry_point("normalizer")

    # Normalizer -> Extractor
    workflow.add_edge("normalizer", "extractor")

    # Extractor -> Intent
    workflow.add_edge("extractor", "intent")

    # Intent -> Router (Conditional)
    workflow.add_conditional_edges(
        "intent",
        route_node,
        {
            "retrieval": END,  # Placeholder for Phase 3: "planner"
            "analytics": END,  # Placeholder for Phase 3: "analytics_planner"
            "end": END,
        },
    )

    # --- Checkpointer ---
    # Using MemorySaver for in-memory durable execution (Session scope)
    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)


# Singleton instance
graph_app = build_graph()
