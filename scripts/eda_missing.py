"""
EDA Missing Values Script - Step 3 (Analyzing Missing Values)

Prints count and percentage of missing values for every column in
wildcat_loans_clean.csv. Then, for credit_score specifically, compares
the distribution of loan_status and loan_purpose among rows where
credit_score is missing vs. the full dataset.
"""

import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    print("=" * 60)
    print("MISSING VALUES: COUNT AND PERCENTAGE PER COLUMN")
    print("=" * 60)
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    missing_summary = pd.DataFrame({"missing_count": missing_count, "missing_pct": missing_pct})
    print(missing_summary)

    missing_credit = df[df["credit_score"].isnull()]

    print()
    print("=" * 60)
    print("loan_status DISTRIBUTION: missing credit_score vs. full dataset")
    print("=" * 60)
    full_status = (df["loan_status"].value_counts(normalize=True) * 100).round(1)
    missing_status = (missing_credit["loan_status"].value_counts(normalize=True) * 100).round(1)
    status_compare = pd.DataFrame({"full_dataset_pct": full_status, "missing_credit_pct": missing_status})
    print(status_compare)

    print()
    print("=" * 60)
    print("loan_purpose DISTRIBUTION: missing credit_score vs. full dataset")
    print("=" * 60)
    full_purpose = (df["loan_purpose"].value_counts(normalize=True) * 100).round(1)
    missing_purpose = (missing_credit["loan_purpose"].value_counts(normalize=True) * 100).round(1)
    purpose_compare = pd.DataFrame({"full_dataset_pct": full_purpose, "missing_credit_pct": missing_purpose})
    print(purpose_compare)


if __name__ == "__main__":
    main()
