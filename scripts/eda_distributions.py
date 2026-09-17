"""
EDA Distribution Analysis Script - Step 6 (Distribution Analysis)

Creates:
  1. A histogram of loan_amount (30 bins) with mean/median lines,
     saved to outputs/hist_loan_amount.png.
  2. A horizontal box plot of interest_rate by loan_status,
     saved to outputs/box_interest_by_status.png.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

STATUS_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]


def make_histogram(df):
    mean_val = df["loan_amount"].mean()
    median_val = df["loan_amount"].median()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["loan_amount"], bins=30, color="#4C72B0", edgecolor="white")
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Mean: ${mean_val:,.2f}")
    ax.axvline(median_val, color="green", linestyle="-", linewidth=2, label=f"Median: ${median_val:,.2f}")
    ax.set_title("Distribution of Loan Amounts – Wildcat Capital Portfolio")
    ax.set_xlabel("Loan Amount ($)")
    ax.set_ylabel("Number of Loans")
    ax.legend()
    fig.tight_layout()

    out_path = OUTPUT_DIR / "hist_loan_amount.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved histogram to {out_path}")
    print(f"Mean loan amount: ${mean_val:,.2f}")
    print(f"Median loan amount: ${median_val:,.2f}")


def make_boxplot(df):
    data = [df.loc[df["loan_status"] == status, "interest_rate"].dropna() for status in STATUS_ORDER]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data, tick_labels=STATUS_ORDER, orientation="horizontal")
    ax.set_title("Interest Rate by Loan Status")
    ax.set_xlabel("Interest Rate (%)")
    ax.set_ylabel("Loan Status")
    fig.tight_layout()

    out_path = OUTPUT_DIR / "box_interest_by_status.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved box plot to {out_path}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    make_histogram(df)
    make_boxplot(df)


if __name__ == "__main__":
    main()
