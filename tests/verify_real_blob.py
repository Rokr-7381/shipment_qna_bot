import os
import sys
from pathlib import Path

import pandas as pd

# Add src to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

# Ensure we are NOT in test mode (delete env var if set)
if "SHIPMENT_QNA_BOT_TEST_MODE" in os.environ:
    del os.environ["SHIPMENT_QNA_BOT_TEST_MODE"]

from shipment_qna_bot.tools.blob_manager import BlobAnalyticsManager


def verify_real_download():
    print("Running REAL integration test against Azure Blob Storage...")

    # Use default cache dir so inspection script can find it
    cache_dir = "data_cache"

    manager = BlobAnalyticsManager(cache_dir=cache_dir)

    print(f"Target Container: {manager.container_name}")
    print(f"Target Blob: {manager.blob_name}")

    try:
        # Download
        file_path = manager.download_master_data()
        print(f"Downloaded to: {file_path}")
        return True
    except Exception as e:
        print(f"FAILURE: {e}")
        return False


if __name__ == "__main__":
    if verify_real_download():
        print("Download Passed")
        sys.exit(0)
    else:
        sys.exit(1)
