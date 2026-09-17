"""
EDA Types Script - Step 2 (Understanding Data Types)

Checks whether origination_date in wildcat_loans_clean.csv is stored as
a datetime type. If it is stored as text (object), converts it to
datetime and prints the before/after types.
"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    before_type = df["origination_date"].dtype
    print(f"origination_date type BEFORE conversion: {before_type}")

    if pd.api.types.is_datetime64_any_dtype(df["origination_date"]):
        print("Column is already datetime. No conversion needed.")
    else:
        df["origination_date"] = pd.to_datetime(df["origination_date"], format="%Y-%m-%d")
        after_type = df["origination_date"].dtype
        print(f"origination_date type AFTER conversion:  {after_type}")
        print(f"Conversion successful: origination_date is now {after_type}.")


if __name__ == "__main__":
    main()
