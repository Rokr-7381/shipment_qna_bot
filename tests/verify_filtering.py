import os
import sys
from pathlib import Path

import pandas as pd

# Add src to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Force production mode for manager to use real file logic
if "SHIPMENT_QNA_BOT_TEST_MODE" in os.environ:
    del os.environ["SHIPMENT_QNA_BOT_TEST_MODE"]

from shipment_qna_bot.tools.blob_manager import BlobAnalyticsManager


def verify_filtering():
    print("Verifying List-Based Filtering...")

    # Use default cache
    manager = BlobAnalyticsManager(cache_dir="data_cache")

    # We saw '0002990' in the inspection output for index 0.
    test_code = "0002990"

    print(f"Filtering for code: {test_code}")
    df = manager.load_filtered_data(consignee_codes=[test_code])

    print(f"Result Rows: {len(df)}")

    if df.empty:
        print("FAILURE: Expected rows for '0002990' but got empty.")
        return False

    # Verify the code is actually in the result
    # Sample check first row
    first_row_codes = df.iloc[0]["consignee_codes"]
    print(f"First Row Codes: {first_row_codes}")

    # Check if '0002990' is in that list
    # Use string check if it returns strings
    found = False
    if isinstance(first_row_codes, list):
        found = test_code in first_row_codes
    elif isinstance(first_row_codes, str):
        found = test_code in first_row_codes
    else:  # numpy array?
        found = test_code in list(first_row_codes)

    if found:
        print("SUCCESS: Filtering logic confirmed.")
        return True
    else:
        print(f"FAILURE: Filtered row does not contain {test_code}.")
        return False


if __name__ == "__main__":
    if verify_filtering():
        sys.exit(0)
    else:
        sys.exit(1)
