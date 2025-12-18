import os
import sys

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Override env var for verification
os.environ["AZURE_SEARCH_CONSIGNEE_IS_COLLECTION"] = "false"
os.environ["AZURE_SEARCH_CONTAINER_FIELD"] = "metadata"

from shipment_qna_bot.tools.azure_ai_search import AzureAISearchTool


def verify():
    try:
        tool = AzureAISearchTool()
    except Exception as e:
        print(f"Failed to init tool: {e}")
        return

    # Provided sample data has:
    # Container: OOCU8049862
    # Consignee: 0025833
    query = "OOCU8049862"
    consignees = ["0025833"]

    print(f"Searching for '{query}' with consignee scope {consignees}...")
    try:
        results = tool.search(query_text=query, consignee_codes=consignees)
        print(f"Found {len(results)} results.")
        if results:
            doc = results[0]
            print("Top result:")
            print(f"  Container: {doc.get('container_number')}")
            print(f"  ID: {doc.get('doc_id')}")
            # print(f"  Content: {doc.get('content')[:100]}...")
        else:
            print(
                "No results found. Indexing might be delayed or search logic mismatch."
            )
    except Exception as e:
        print(f"Search failed: {e}")


if __name__ == "__main__":
    verify()
