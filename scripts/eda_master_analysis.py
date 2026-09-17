"""
Master EDA Analysis - Wildcat Capital Loan Portfolio

Combines all individual EDA scripts (eda_inspect, eda_types, eda_missing,
eda_summary_stats, eda_categorical, eda_distributions, eda_grouping,
eda_correlations) into a single program that runs the full 8-step EDA
tutorial workflow against wildcat_loans_clean.csv in one pass.

Run with:
    python scripts/eda_master_analysis.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Data" / "Raw" / "wildcat_loans_clean.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

CATEGORICAL_COLUMNS = ["loan_purpose", "loan_status", "state"]
STATUS_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]
STATUS_COLORS = {
    "Current": "#4C72B0",
    "Paid Off": "#55A868",
    "Delinquent": "#DD8452",
    "Default": "#C44E52",
}
CORRELATION_EXCLUDE_COLUMNS = ["loan_id", "borrower_id"]

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def section(title):
    print()
    print("#" * 70)
    print(f"# {title}")
    print("#" * 70)


def step1_inspect(df):
    section("STEP 1 - LOADING AND INSPECTING THE DATA")

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


def step2_types(df):
    section("STEP 2 - UNDERSTANDING DATA TYPES")

    before_type = df["origination_date"].dtype
    print(f"origination_date type BEFORE conversion: {before_type}")

    if pd.api.types.is_datetime64_any_dtype(df["origination_date"]):
        print("Column is already datetime. No conversion needed.")
    else:
        df["origination_date"] = pd.to_datetime(df["origination_date"], format="%Y-%m-%d")
        after_type = df["origination_date"].dtype
        print(f"origination_date type AFTER conversion:  {after_type}")
        print(f"Conversion successful: origination_date is now {after_type}.")

    return df


def step3_missing(df):
    section("STEP 3 - ANALYZING MISSING VALUES")

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


def step4_summary_stats(df):
    section("STEP 4 - SUMMARY STATISTICS")

    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe().round(2)

    print("=" * 60)
    print("SUMMARY STATISTICS: NUMERIC COLUMNS")
    print("=" * 60)
    print(stats)


def step5_categorical(df):
    section("STEP 5 - EXPLORING CATEGORICAL VARIABLES")

    for col in CATEGORICAL_COLUMNS:
        print("=" * 60)
        print(f"{col.upper()} DISTRIBUTION")
        print("=" * 60)
        counts = df[col].value_counts()
        pct = (df[col].value_counts(normalize=True) * 100).round(1)
        summary = pd.DataFrame({"count": counts, "pct": pct})
        print(summary)
        print()


def step6_distributions(df):
    section("STEP 6 - DISTRIBUTION ANALYSIS")

    # Histogram: loan_amount with mean/median lines
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

    # Box plot: interest_rate by loan_status
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


def step7_grouping(df):
    section("STEP 7 - GROUPING AND AGGREGATION")

    grouped_status = df.groupby("loan_status").agg(
        count=("loan_status", "size"),
        mean_loan_amount=("loan_amount", "mean"),
        mean_interest_rate=("interest_rate", "mean"),
        mean_credit_score=("credit_score", "mean"),
        mean_debt_to_income_ratio=("debt_to_income_ratio", "mean"),
    )
    grouped_status["mean_loan_amount"] = grouped_status["mean_loan_amount"].round(2)
    grouped_status["mean_interest_rate"] = grouped_status["mean_interest_rate"].round(4)
    grouped_status["mean_credit_score"] = grouped_status["mean_credit_score"].round(1)
    grouped_status["mean_debt_to_income_ratio"] = grouped_status["mean_debt_to_income_ratio"].round(4)
    grouped_status = grouped_status.sort_values("count", ascending=False)

    print("=" * 60)
    print("GROUPED BY loan_status")
    print("=" * 60)
    print(grouped_status)

    grouped_purpose = df.groupby("loan_purpose").agg(count=("loan_purpose", "size"))
    default_counts = df[df["loan_status"] == "Default"].groupby("loan_purpose").size()
    grouped_purpose["default_count"] = grouped_purpose.index.map(default_counts).fillna(0).astype(int)
    grouped_purpose["default_pct"] = (grouped_purpose["default_count"] / grouped_purpose["count"] * 100).round(1)
    grouped_purpose = grouped_purpose.sort_values("default_pct", ascending=False)

    print()
    print("=" * 60)
    print("GROUPED BY loan_purpose - DEFAULT RATE")
    print("=" * 60)
    print(grouped_purpose)


def step8_correlations(df):
    section("STEP 8 - RELATIONSHIPS BETWEEN VARIABLES")

    numeric_df = df.select_dtypes(include="number").drop(columns=CORRELATION_EXCLUDE_COLUMNS)
    corr = numeric_df.corr().round(2)

    print("=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)
    print(corr)

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

    step1_inspect(df)
    df = step2_types(df)
    step3_missing(df)
    step4_summary_stats(df)
    step5_categorical(df)
    step6_distributions(df)
    step7_grouping(df)
    step8_correlations(df)

    section("EDA COMPLETE")
    print(f"Charts saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
