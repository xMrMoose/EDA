"""
EDA Inspect Script - Week 2 Exercise

Loads wildcat_loans_clean.csv into a pandas DataFrame and prints:
  - shape (rows and columns)
  - all column names with their data types
  - count of missing values for every column
"""

import pandas as pd
from pathlib import Path

# Path to the CSV file, relative to the project root
DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    print("=" * 60)
    print("SHAPE")
    print("=" * 60)
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print()
    print("=" * 60)
    print("COLUMN NAMES AND DATA TYPES")
    print("=" * 60)
    print(df.dtypes)

    print()
    print("=" * 60)
    print("MISSING VALUES PER COLUMN")
    print("=" * 60)
    print(df.isnull().sum())


if __name__ == "__main__":
    main()
