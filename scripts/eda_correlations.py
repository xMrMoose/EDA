"""
EDA Relationships Script - Step 8 (Relationships Between Variables)

1. Computes the correlation matrix for all numeric columns (excluding
   loan_id and borrower_id), rounded to two decimal places, and
   identifies the three strongest correlations.
2. Creates a scatter plot of credit_score vs. interest_rate, colored by
   loan_status, saved to outputs/scatter_credit_rate.png.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

EXCLUDE_COLUMNS = ["loan_id", "borrower_id"]
STATUS_COLORS = {
    "Current": "#4C72B0",
    "Paid Off": "#55A868",
    "Delinquent": "#DD8452",
    "Default": "#C44E52",
}


def compute_correlations(df):
    numeric_df = df.select_dtypes(include="number").drop(columns=EXCLUDE_COLUMNS)
    corr = numeric_df.corr().round(2)

    print("=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)
    print(corr)

    # Find the three strongest correlations (excluding self-correlation and duplicate pairs)
    pairs = []
    cols = corr.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append((cols[i], cols[j], corr.iloc[i, j]))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    print()
    print("=" * 60)
    print("THREE STRONGEST CORRELATIONS")
    print("=" * 60)
    for col_a, col_b, value in pairs[:3]:
        print(f"{col_a} <-> {col_b}: {value}")


def make_scatter(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    for status, color in STATUS_COLORS.items():
        subset = df[df["loan_status"] == status]
        ax.scatter(subset["credit_score"], subset["interest_rate"], label=status, color=color, alpha=0.6, s=15)

    ax.set_title("Credit Score vs. Interest Rate by Loan Status")
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Interest Rate (%)")
    ax.legend(title="Loan Status")
    fig.tight_layout()

    out_path = OUTPUT_DIR / "scatter_credit_rate.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"\nSaved scatter plot to {out_path}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    compute_correlations(df)
    make_scatter(df)


if __name__ == "__main__":
    main()
