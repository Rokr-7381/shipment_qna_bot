import os
import sys
from pathlib import Path

import pandas as pd

# Add src to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Force test mode for deterministic data
os.environ["SHIPMENT_QNA_BOT_TEST_MODE"] = "true"

from shipment_qna_bot.tools.blob_manager import BlobAnalyticsManager
from shipment_qna_bot.tools.pandas_engine import PandasAnalyticsEngine


def test_full_analytics_flow():
    print("Testing Full Analytics Flow (Manager + Engine)...")

    # 1. Initialize Components
    cache_dir = "tests/flow_cache"
    blob_mgr = BlobAnalyticsManager(cache_dir=cache_dir)
    engine = PandasAnalyticsEngine()

    # 2. Load Data (Test Mode = Mock Data)
    # Mock data created by BlobManager in test mode:
    # {"id": "1", "consignee_code": "TEST", "status": "DELIVERED"},
    # {"id": "2", "consignee_code": "OTHER", "status": "IN_OCEAN"}
    print("Step 1: Loading Data...")
    df = blob_mgr.load_filtered_data(consignee_codes=["TEST"])

    if df.empty:
        print("FAILURE: DataFrame is empty.")
        return False

    print(f"Loaded {len(df)} rows.")

    # 3. Define Analysis Code
    # Let's count status for "TEST" consignee
    code = """
# Calculate status counts
result = df['status'].value_counts()
"""

    # 4. Execute
    print("Step 2: Executing Pandas Code...")
    response = engine.execute_code(df, code)

    if not response["success"]:
        print(f"FAILURE: Execution error: {response['error']}")
        return False

    print(f"Result:\n{response['result']}")

    # 5. Verify
    # Expect: DELIVERED 1 (since "OTHER" row is filtered out)
    res_str = str(response["result"])
    if "DELIVERED" in res_str and "1" in res_str:
        if "IN_OCEAN" in res_str:
            print(
                "FAILURE: Leakage! 'IN_OCEAN' (from OTHER consignee) found in result."
            )
            return False
        print("SUCCESS: Flow Verified. Correctly filtered and aggregated.")
        return True
    else:
        print("FAILURE: Expected 'DELIVERED 1' not found.")
        return False


if __name__ == "__main__":
    if test_full_analytics_flow():
        sys.exit(0)
    else:
        sys.exit(1)
