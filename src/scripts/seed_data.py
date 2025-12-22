import json
import os
import sys
from typing import Any, Dict, List

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from shipment_qna_bot.tools.azure_ai_search import AzureAISearchTool


def load_data(file_path: str) -> List[Dict[str, Any]]:
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                documents.append(record)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {e}")
    return documents


def normalize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize document fields to match Azure Search index schema.
    Expects env vars to match, but here we enforce the schema.
    """
    # 1. ID field
    # Tool uses AZURE_SEARCH_ID_FIELD, default "chunk_id".
    # Data has "document_id".
    doc_id = doc.get("document_id")

    # 2. Content field
    # Tool uses AZURE_SEARCH_CONTENT_FIELD, default "chunk".
    # Data has "content".
    content = doc.get("content")

    # 3. Container field
    # Tool uses AZURE_SEARCH_CONTAINER_FIELD, default "container_number".
    # Data has "container_number" in "metadata", or sometimes top level?
    # Let's check metadata first.
    metadata = doc.get("metadata", {})
    container_number = metadata.get("container_number")
    if not container_number:
        # Try to extract from content if missing?
        pass

    # 4. Consignee field
    # Tool uses AZURE_SEARCH_CONSIGNEE_FIELD, default "consignee_codes".
    # Data has "consignee_code" (string rep of list) at top level,
    # AND "consignee_codes" (list of strings) in metadata.
    # We prefer metadata.
    consignee_codes = metadata.get("consignee_codes", [])
    if not consignee_codes:
        # Fallback to top-level 'consignee_code' which looks like "['0025833']"
        raw_code = doc.get("consignee_code")
        if raw_code and isinstance(raw_code, str):
            try:
                # safe eval or json load? it uses single quotes, valid python, invalid json
                # generic replace
                cleaned = raw_code.replace("'", '"')
                consignee_codes = json.loads(cleaned)
            except Exception:
                # simple fallback
                consignee_codes = [raw_code]

    # Construct new doc matching expected schema
    # We default target fields to what the tool expects by default
    # But usually we map to what the INDEX has.
    # Index has: chunk_id, chunk, container_number, consignee_codes

    # Construct new doc matching expected schema using inspected keys
    # Index fields: chunk_id, chunk, document_id, metadata, consignee_code, etc.

    # Map container_number into metadata
    if container_number:
        # Assuming metadata is a dict derived from 'metadata' field in input
        if "container_number" not in metadata:
            metadata["container_number"] = container_number

    # Map consignee_codes (list) to consignee_code (string)
    # Taking the first one or joining? Index implies singular string.
    consignee_val = None
    if consignee_codes and isinstance(consignee_codes, list):
        consignee_val = consignee_codes[0]  # Take first for now
    elif consignee_codes and isinstance(consignee_codes, str):
        consignee_val = consignee_codes

    new_doc = {
        "chunk_id": doc_id,  # using document_id as chunk_id
        "chunk": content,
        "document_id": doc_id,
        "metadata": metadata,  # ComplexType
        "consignee_code": consignee_val,
        # "text_vector": [] # Optional?
    }

    # remove None keys if index doesn't support nulls?
    # Consignee codes is collection, required.
    return new_doc


def main():
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "shipments.jsonl"
    )
    if not os.path.exists(data_path):
        print(f"Data file not found: {data_path}")
        return

    raw_docs = load_data(data_path)
    print(f"Loaded {len(raw_docs)} documents from {data_path}")

    normalized_docs = [normalize_document(d) for d in raw_docs]

    print("Initializing AzureAISearchTool...")
    try:
        tool = AzureAISearchTool()
    except Exception as e:
        print(f"Failed to init tool: {e}")
        return

    print("Uploading documents...")
    try:
        tool.upload_documents(normalized_docs)
        print("Upload successful!")
    except Exception as e:
        print(f"Upload failed: {e}")


if __name__ == "__main__":
    main()
