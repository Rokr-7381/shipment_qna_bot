from operator import add
from typing import Annotated, Any, Dict, List, Optional, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of the conversation graph.
    """

    # --- Input ---
    question: str
    normalized_question: Optional[str]

    # --- Context ---
    conversation_id: str
    trace_id: str
    allowed_consignee_codes: List[str]

    # --- Extraction ---
    # We use 'add' reducer to accumulate entities if multiple nodes find them (though usually just one extractor)
    # For now, simple overwrite is fine, but 'add' is safer for lists.
    extracted_ids: Dict[str, List[str]]  # e.g. {'container': ['ABCD123'], 'po': []}
    time_window_days: Optional[int]

    # --- Intent ---
    primary_intent: Optional[str]
    sub_intents: List[str]

    # --- Retrieval ---
    retrieval_plan: Optional[Dict[str, Any]]
    retrieved_docs: List[Dict[str, Any]]

    # --- Output ---
    final_answer: Optional[str]
    citations: List[Dict[str, Any]]
    chart_spec: Optional[Dict[str, Any]]

    # --- Errors/Notices ---
    errors: Annotated[List[str], add]
    notices: Annotated[List[str], add]
