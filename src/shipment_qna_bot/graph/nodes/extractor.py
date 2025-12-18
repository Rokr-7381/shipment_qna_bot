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
    # Container: 4 letters + 7 digits (e.g., ABCD1234567)
    container_pattern = r"\b[a-zA-Z]{4}\d{7}\b"
    # PO: Prefix PO + digits (e.g., PO12345) - illustrative
    po_pattern = r"\bPO\d{5,10}\b"
    # OBL: Prefix OBL + alphanumeric (e.g., OBLABCD123) - illustrative
    obl_pattern = r"\bOBL[a-zA-Z0-9]{5,12}\b"

    containers = [c.upper() for c in re.findall(container_pattern, text)]
    pos = [p.upper() for p in re.findall(po_pattern, text, re.IGNORECASE)]
    obls = [o.upper() for o in re.findall(obl_pattern, text, re.IGNORECASE)]

    extracted = {
        "container": containers,
        "po": pos,
        "obl": obls,
    }

    count = sum(len(v) for v in extracted.values())
    logger.info(
        f"Extracted {count} entities", extra={"extra_data": {"extracted": extracted}}
    )

    return {"extracted_ids": extracted}
