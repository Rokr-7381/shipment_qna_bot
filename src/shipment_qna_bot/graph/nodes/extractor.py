import re
from typing import Dict, List

from shipment_qna_bot.graph.state import GraphState
from shipment_qna_bot.logging.logger import logger


def extractor_node(state: GraphState) -> GraphState:
    """
    Extracts entities (Container, PO, OBL) from the normalized question.
    """
    text = state.get("normalized_question", "")

    # Regex patterns (simplified for demo)
    # Container: 4 letters + 7 digits (e.g., ABCD1234567)
    container_pattern = r"[a-z]{4}\d{7}"

    containers = [c.upper() for c in re.findall(container_pattern, text)]

    extracted = {
        "container": containers,
        "po": [],  # TODO: Add PO pattern
        "obl": [],  # TODO: Add OBL pattern
    }

    count = sum(len(v) for v in extracted.values())
    logger.info(
        f"Extracted {count} entities", extra={"extra_data": {"extracted": extracted}}
    )

    return {"extracted_ids": extracted}
