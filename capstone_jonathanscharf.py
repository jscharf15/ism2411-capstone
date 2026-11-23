"""
ISM2411 Capstone — Small-Business Loan Portfolio Analysis
Author: Jonathan Scharf
Date:   December 6, 2026

Business Questions:
  1. [Your question 1]
  2. [Your question 2]
  3. [Your question 3]

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

# Duplicates: 40 rows were exact copies of the same loan, so keeping them would count those loans twice
df = df.drop_duplicates()
print("After duplicates:", df.shape)

# Money: loan_amount and profit are text because of $ and ,
# Remove them and convert to numbers (negatives like -$45.00 stay negative)
# Fix loan_amount: strip "$" and ",", convert to float
df["loan_amount"] = df["loan_amount"].str.replace("$", "", regex=False)
df["loan_amount"] = df["loan_amount"].str.replace(",", "", regex=False).astype(float)

# Fix profit: strip "$" and ",", convert to float (negatives like -$45.00 stay negative)
df["profit"] = df["profit"].str.replace("$", "", regex=False)
df["profit"] = df["profit"].str.replace(",", "", regex=False).astype(float)

# Dates: most parse directly. Recover the other real formats (MM/DD/YYYY and "March 29 2025") 
# Junk like "TBD" and impossible dates like 2025-13-01 stay NaT because there is no real date to recover
raw_dates = df["application_date"].copy()
d1 = pd.to_datetime(raw_dates, errors="coerce")
d2 = pd.to_datetime(raw_dates, format="%m/%d/%Y", errors="coerce")
d3 = pd.to_datetime(raw_dates, format="%B %d %Y", errors="coerce")
df["application_date"] = d1.fillna(d2).fillna(d3)
print("NaT count:", df["application_date"].isna().sum())

# Industry typos: fix capitals and spaces first, then the two misspellings
df["industry"] = df["industry"].str.strip().str.title()
df["industry"] = df["industry"].replace({"Resturants": "Restaurants",
                                         "Constrction": "Construction"})
print(df["industry"].value_counts())

# Impossible values: 9,999 employees is a fake placeholder.
# Set to blank instead of deleting the row because the loan data is still good
# Checked the largest remaining counts (415, 381, 313...) 
# They taper off gradually, so they look like real businesses.
df["employees"] = df["employees"].mask(df["employees"] == 9999)

# Missing values: region filled with "Unknown" so the loans stay in the data
# credit_score and application_date left blank on purpose, because filling them would invent scores and dates.
df["region"] = df["region"].fillna("Unknown")

# Negative amounts: kept on purpose. Only Default loans have negative profit (money lost)  
# Every other status is positive
print(df.groupby("loan_status")["profit"].agg(["count", "min", "max"]))

# Final check: shape and blanks after cleaning
print("Clean shape:", df.shape)
print(df.isnull().sum())

# ── 3. DERIVED COLUMNS ────────────────────────────────────────
# [Add any columns your questions need, with a comment on why]

# ── 4. DESCRIPTIVE SUMMARY ────────────────────────────────────
print("\nDescriptive stats (clean):")
print(df.describe())

# ── 5. BUSINESS QUESTION 1 ────────────────────────────────────
# [State your question in a comment]
# [Your analysis code here]
# [Your chart code here — with title, axis labels, savefig, show]
# [Write a one-sentence finding in a comment]

# ── 6. BUSINESS QUESTION 2 ────────────────────────────────────
# [State your question]
# [Analysis + chart]

# ── 7. BUSINESS QUESTION 3 ────────────────────────────────────
# [State your question]
# [Analysis + chart]

# ── 8. SAVE CLEAN DATA ────────────────────────────────────────
df.to_csv("data/clean_data.csv", index=False)
print("\nCapstone complete. Clean data saved to data/clean_data.csv")
