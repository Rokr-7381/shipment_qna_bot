import pytest

from shipment_qna_bot.graph.builder import graph_app
from shipment_qna_bot.graph.state import GraphState


def test_graph_compilation():
    """
    Verifies that the graph compiles without errors.
    """
    assert graph_app is not None


def test_graph_routing_eta():
    """
    Verifies that 'eta' keyword routes to 'retrieval' path (which ends for now).
    """
    initial_state = {
        "question": "What is the ETA for container ABCD1234567?",
        "conversation_id": "test_conv",
        "trace_id": "test_trace",
        "allowed_consignee_codes": ["TEST"],
    }

    # We run the graph. Since "retrieval" node is not added yet, it should hit END after router.
    # But wait, in builder.py we mapped "retrieval" -> END. So it should finish.

    # We need to configure the thread for the checkpointer
    config = {"configurable": {"thread_id": "test_thread"}}

    result = graph_app.invoke(initial_state, config=config)

    assert result["normalized_question"] == "what is the eta for container abcd1234567?"
    assert result["primary_intent"] == "eta"
    # Extractor should find the container
    assert "ABCD1234567" in result["extracted_ids"]["container"]


def test_graph_routing_analytics():
    """
    Verifies that 'chart' keyword routes to 'analytics' path.
    """
    initial_state = {
        "question": "Show me a chart of delays",
        "conversation_id": "test_conv",
        "trace_id": "test_trace",
        "allowed_consignee_codes": ["TEST"],
    }
    config = {"configurable": {"thread_id": "test_thread_2"}}

    result = graph_app.invoke(initial_state, config=config)

    assert result["primary_intent"] == "analytics"
