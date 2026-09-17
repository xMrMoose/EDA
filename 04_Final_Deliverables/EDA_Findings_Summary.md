# Wildcat Capital Loan Portfolio — EDA Findings Summary

**Dataset:** `wildcat_loans_clean.csv` | **Scope:** Loan portfolio only (2,340 loans, 12 attributes)

## Dataset Overview

The portfolio contains 2,340 individual loans, each described by 12 attributes covering loan terms, borrower creditworthiness, and current loan performance. This is the primary, cleanest file in the broader Wildcat Capital dataset and the population this EDA covers.

## Data Quality Issues

- **Missing credit scores:** 47 loans (2.0%) have no recorded credit score. Critically, this missingness is **not random** — loans with a missing credit score are disproportionately Delinquent or Default (34.0% combined) compared to the full portfolio (15.1% combined). Any credit-risk analysis that simply drops these rows would understate portfolio risk and should account for this instead.
- **State column has duplicate categories:** 7 states (PA, NJ, NY, FL, CA, IL, TX) are each split across two labels — a two-letter abbreviation and the full state name (e.g., "PA" and "Pennsylvania" recorded separately). This must be standardized before any state-level analysis, or those states' totals will be understated.
- **origination_date required a type conversion:** it was stored as text and has been converted to a proper date type so date-based analysis (filtering, month/year extraction) is possible. No other column required correction.
- No other data quality issues were found: no negative loan amounts, no out-of-range credit scores (500–850, a valid range), no debt-to-income ratios outside 0–1, and no implausible interest rates.

## Key Distributions

- The **typical loan** is roughly $40,700 (median), with a term concentrated between 36 and 84 months, at a median interest rate of 11.5%.
- **Loan amount is right-skewed**: the average ($68,400) is well above the typical loan, pulled up by a smaller number of much larger loans.
- **Annual income is even more right-skewed**: the average ($155,100) is nearly 4x the typical borrower's income ($42,600), driven by a small group of very high earners. The median, not the average, best represents the typical Wildcat Capital borrower on both of these measures.

## Categorical Breakdown

- **Loan purpose:** Home Improvement is the largest category (30.9% of loans), followed by Auto (25.8%), Personal (20.3%), Business (14.0%), and Education (9.0%).
- **Loan status — default rate called out:** 62.1% of loans are Current, 22.7% are Paid Off, 10.6% are Delinquent, and **4.5% (106 loans) are in Default**. Combined, 15.1% of the portfolio (354 loans) is either delinquent or in default and warrants active monitoring.

## Notable Relationships

- **Credit score and interest rate are strongly negatively correlated (-0.84)** — higher-credit borrowers reliably receive lower rates, confirming the rate-setting process works as intended. This is by far the strongest relationship in the dataset; every other pair of numeric variables is essentially uncorrelated.
- **Default loans have a materially lower average credit score** (617 vs. 685 for Current loans) **and a higher average interest rate** (14.2% vs. 11.3%). Delinquent and Paid Off loans fall in between, in that order — credit score and interest rate both look like promising inputs for a future default-risk model.
- **Home Improvement loans default at nearly 3x the rate of Education loans** (6.5% vs. 2.4%), and Home Improvement is also the single largest loan category by volume — this combination (high volume + high default rate) makes it the most consequential purpose category for origination policy to review.
- **Interest rates appear to be set in tiers, not on a smooth scale.** The credit score vs. interest rate scatter plot shows rates clustering into distinct bands aligned with credit score ranges rather than declining gradually — consistent with a tiered rate-card pricing structure. Worth confirming with the lending team, since it changes how credit score should be modeled (as a category, not a continuous number) in any future pricing or risk work.

## Open Questions and Next Steps

- Whether the missing-credit-score pattern reflects a data collection gap tied to riskier borrowers, or a separate process issue, would need to be investigated with the loan origination team before deciding how to treat those 47 rows in downstream risk models.
- The correlation and grouped findings above are exploratory, not causal — they identify credit score and interest rate as the leading candidate signals for a formal default-risk model, but do not establish which (if either) drives default risk versus simply correlating with it.
- Before any state-level reporting, the state column's duplicate abbreviation/full-name categories need to be standardized.
- A parallel EDA pass on `wildcat_loans_raw.csv` (the intentionally dirtier 2,420-row version) would be a useful exercise for data-cleaning practice, since it contains duplicates and additional formatting issues not present in this clean file.

## Reference: Scripts and Outputs

| Step | Script | Results |
|---|---|---|
| 1. Load & Inspect | `scripts/eda_inspect.py` | `03_Drafts/eda_inspect_results.md` |
| 2. Data Types | `scripts/eda_types.py` | `03_Drafts/eda_types_results.md` |
| 3. Missing Values | `scripts/eda_missing.py` | `03_Drafts/eda_missing_results.md` |
| 4. Summary Statistics | `scripts/eda_summary_stats.py` | `03_Drafts/eda_summary_stats_results.md` |
| 5. Categorical Variables | `scripts/eda_categorical.py` | `03_Drafts/eda_categorical_results.md` |
| 6. Distribution Analysis | `scripts/eda_distributions.py` | `03_Drafts/eda_distributions_results.md`, `outputs/hist_loan_amount.png`, `outputs/box_interest_by_status.png` |
| 7. Grouping & Aggregation | `scripts/eda_grouping.py` | `03_Drafts/eda_grouping_results.md` |
| 8. Relationships | `scripts/eda_correlations.py` | `03_Drafts/eda_correlations_results.md`, `outputs/scatter_credit_rate.png` |
