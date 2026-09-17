"""
EDA Summary Statistics Script - Step 4 (Summary Statistics)

Prints descriptive statistics (count, mean, std, min, 25%, 50%, 75%, max)
for all numeric columns in wildcat_loans_clean.csv. Loan amounts are
rounded to two decimal places.
"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"

pd.set_option("display.float_format", lambda x: f"{x:.2f}")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def main():
    df = pd.read_csv(DATA_PATH)

    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe().round(2)

    print("=" * 60)
    print("SUMMARY STATISTICS: NUMERIC COLUMNS")
    print("=" * 60)
    print(stats)


if __name__ == "__main__":
    main()
