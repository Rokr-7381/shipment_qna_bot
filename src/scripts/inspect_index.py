import os
import sys

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient


def inspect_index():
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

    if not endpoint or not index_name:
        print("Missing env vars")
        return

    cred = AzureKeyCredential(api_key) if api_key else DefaultAzureCredential()
    client = SearchIndexClient(endpoint=endpoint, credential=cred)

    try:
        index = client.get_index(index_name)
        print(f"Index: {index.name}")
        print("Fields:")
        for field in index.fields:
            print(f"- {field.name} (Type: {field.type})")
    except Exception as e:
        print(f"Error getting index: {e}")


if __name__ == "__main__":
    inspect_index()
