import os
import sys
from pathlib import Path

import pandas as pd

from shipment_qna_bot.tools.date_tools import get_today_date

# Add src to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))


def inspect_columns():
    cache_dir = "data_cache"
    file_path = os.path.join(cache_dir, f"master_{get_today_date()}.parquet")

    if not os.path.exists(file_path):
        import glob

        files = glob.glob(os.path.join(cache_dir, "master_*.parquet"))
        if files:
            # Sort by modification time to get the latest
            files.sort(key=os.path.getmtime, reverse=True)
            file_path = files[0]
            print(f"Using latest file: {file_path}")
        else:
            print("No master file found.")
            return

    try:
        df = pd.read_parquet(file_path)
        cols = list(df.columns)
        print(f"File: {os.path.basename(file_path)}")
        print(f"Columns ({len(cols)}): {cols}")

        target = "consignee_codes"
        if target in cols:
            print(f"SUCCESS: Column '{target}' FOUND.")
            print(df[target].head(5))
        else:
            print(f"FAILURE: Column '{target}' NOT FOUND.")
            # print close matches
            print("Close matches:", [c for c in cols if "consignee" in c.lower()])

    except Exception as e:
        print(f"Error reading parquet: {e}")


if __name__ == "__main__":
    inspect_columns()
