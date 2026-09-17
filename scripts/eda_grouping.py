"""
EDA Grouping and Aggregation Script - Step 7 (Grouping and Aggregation)

1. Groups by loan_status: count, mean loan_amount, mean interest_rate,
   mean credit_score (excluding nulls), mean debt_to_income_ratio.
   Sorted by count descending.
2. Groups by loan_purpose: count of loans and number/percentage with
   loan_status == "Default". Sorted by default percentage descending.
"""

import pandas as pd
from pathlib import Path

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"


def group_by_status(df):
    grouped = df.groupby("loan_status").agg(
        count=("loan_status", "size"),
        mean_loan_amount=("loan_amount", "mean"),
        mean_interest_rate=("interest_rate", "mean"),
        mean_credit_score=("credit_score", "mean"),
        mean_debt_to_income_ratio=("debt_to_income_ratio", "mean"),
    )
    grouped["mean_loan_amount"] = grouped["mean_loan_amount"].round(2)
    grouped["mean_interest_rate"] = grouped["mean_interest_rate"].round(4)
    grouped["mean_credit_score"] = grouped["mean_credit_score"].round(1)
    grouped["mean_debt_to_income_ratio"] = grouped["mean_debt_to_income_ratio"].round(4)
    grouped = grouped.sort_values("count", ascending=False)

    print("=" * 60)
    print("GROUPED BY loan_status")
    print("=" * 60)
    print(grouped)


def group_by_purpose(df):
    grouped = df.groupby("loan_purpose").agg(count=("loan_purpose", "size"))
    default_counts = df[df["loan_status"] == "Default"].groupby("loan_purpose").size()
    grouped["default_count"] = grouped.index.map(default_counts).fillna(0).astype(int)
    grouped["default_pct"] = (grouped["default_count"] / grouped["count"] * 100).round(1)
    grouped = grouped.sort_values("default_pct", ascending=False)

    print()
    print("=" * 60)
    print("GROUPED BY loan_purpose - DEFAULT RATE")
    print("=" * 60)
    print(grouped)


def main():
    df = pd.read_csv(DATA_PATH)
    group_by_status(df)
    group_by_purpose(df)


if __name__ == "__main__":
    main()
