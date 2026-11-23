"""
ISM2411 Capstone — Small-Business Loan Portfolio Analysis
Author: Jonathan Scharf
Date:   December 6, 2026

Business Questions:
  1. How does the default rate change as credit scores fall, and do lower-score borrowers still earn the bank a profit on average?
  2. Which industries make the bank the most profit per loan, and is that because they default less often?
  3. Do larger loans default more often than smaller ones, and do they account for most of the bank's losses?

AI Disclosure: 
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# ── 1. LOAD ───────────────────────────────────────────────────
# Load the raw data and look at it before changing anything
DATA_FILE = "data/capstone_finance.csv"
df = pd.read_csv(DATA_FILE)
print("Raw shape:", df.shape)
print(df.head())
df.info()
print(df.isnull().sum())
print(df.describe())

# -- M13: DATA QUALITY ISSUES (raw: 5,000 rows x 11 columns) --
# 1. Blank cells: Region (128), Credit Score (91), Application Date (30)
# 2. Wrong types: Loan Amount and Profit are text because of "$" and ","
#    Application Date is text, not a date.
# 3. Weird numbers: Employees has 9,999, which looks fake.
#    Employees of 0 is okay (some businesses have no workers).
# 4. Duplicates: 40 rows are exact copies.
# 5. Industry names: there are 40+ spellings instead of 8
#    (different capitals, extra spaces, typos like "Resturants")
#    Region and Loan Status are fine.

# ── 2. CLEAN ──────────────────────────────────────────────────
# Column names: lowercase with underscores so they are easier to type
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Drop rows missing essential identifiers
# Reason: a loan can't be placed in time without an application date
df = df.dropna(subset=["application_date"])

# Dates: most parse directly. Recover the other real formats (MM/DD/YYYY and "March 29 2025") 
# Junk like "TBD" and impossible dates like 2025-13-01 stay NaT because there is no real date to recover
raw_dates = df["application_date"].copy()
d1 = pd.to_datetime(raw_dates, errors="coerce")
d2 = pd.to_datetime(raw_dates, format="%m/%d/%Y", errors="coerce")
d3 = pd.to_datetime(raw_dates, format="%B %d %Y", errors="coerce")
df["application_date"] = d1.fillna(d2).fillna(d3)
print("NaT count:", df["application_date"].isna().sum())

# Money: loan_amount and profit are text because of $ and ,
# Remove them and convert to numbers
# Fix loan_amount: strip "$" and ",", convert to float
df["loan_amount"] = df["loan_amount"].str.replace("$", "", regex=False)
df["loan_amount"] = df["loan_amount"].str.replace(",", "", regex=False).astype(float)

# Fix profit: strip "$" and ",", convert to float 
df["profit"] = df["profit"].str.replace("$", "", regex=False)
df["profit"] = df["profit"].str.replace(",", "", regex=False).astype(float)

# Negative profit: kept on purpose. Only Default loans have negative profit (money lost)  
# Reason: negative profit is money lost on a defaulted loan, and those losses are important to this dataset
# Only Default loans are negative
print(df.groupby("loan_status")["profit"].agg(["count", "min", "max"]))

# Remove impossible values that describe() reveals
# Reason: 9,999 employees is a placeholder someone typed, not a real business
df = df[df["employees"] != 9999]

# Fill missing credit_score with median (about 2% of rows, aggregate impact minimal)
df["credit_score"] = df["credit_score"].fillna(df["credit_score"].median())

# Fill missing region with "Unknown" so the loans stay in the data
df["region"] = df["region"].fillna("Unknown")

# Industry typos: fix capitals and spaces first, then the two misspellings that value_counts() shows
df["industry"] = df["industry"].str.strip().str.title()
df["industry"] = df["industry"].replace(
    {"Resturants": "Restaurants", "Constrction": "Construction"}
)
print(df["industry"].value_counts())

# Remove duplicates: 40 rows were exact copies of the same loan
df = df.drop_duplicates()
print("Clean shape:", df.shape)
print(df.isnull().sum())

# ── 3. DERIVED COLUMNS ────────────────────────────────────────
# ---- Question 1 ----
# credit_band: groups scores into standard FICO-style ranges so default rate
# can be compared across them
df["credit_band"] = pd.cut(
    df["credit_score"],
    bins=[300, 580, 670, 740, 800, 851],
    labels=["Poor (<580)", "Fair (580-669)", "Good (670-739)",
            "Very Good (740-799)", "Exceptional (800+)"],
    right=False,
)

# is_default: 1 if the loan defaulted, 0 if not, so the average is the default rate
df["is_default"] = (df["loan_status"] == "Default").astype(int)

# --- Question 2 ----

# ---- Question 3 ----

# ── 4. DESCRIPTIVE SUMMARY ────────────────────────────────────
print("\nDescriptive stats (clean):")
print(df.describe())

# ── 5. BUSINESS QUESTION 1 ────────────────────────────────────
# How does the default rate change as credit scores fall, and do lower-score borrowers still earn the bank a profit on average?
# "Default rate" is the share of loans with loan_status == "Default"


# [Your analysis code here]
# [Your chart code here — with title, axis labels, savefig, show]
# [Write a one-sentence finding in a comment]

# ── 6. BUSINESS QUESTION 2 ────────────────────────────────────
# Which industries make the bank the most profit per loan, and is that because they default less often?
# [Analysis + chart]

# ── 7. BUSINESS QUESTION 3 ────────────────────────────────────
# Do larger loans default more often than smaller ones, and do they account for most of the bank's losses?
# [Analysis + chart]

# ── 8. SAVE CLEAN DATA ────────────────────────────────────────
df.to_csv("data/clean_data.csv", index=False)
print("\nCapstone complete. Clean data saved to data/clean_data.csv")
