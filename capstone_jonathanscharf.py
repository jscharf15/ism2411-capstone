import pandas as pd

df = pd.read_csv("data/capstone_finance.csv")
print(df.shape)
print(df.head())
df.info()
print(df.isnull().sum())
print(df.describe())

# ── M13: DATA QUALITY ISSUES (raw: 5,000 rows x 11 columns) ──
# 1. Blank cells: Region (128), Credit Score (91), Application Date (30)
# 2. Wrong types: Loan Amount and Profit are text because of "$" and ",".
#    Application Date is text, not a date.
# 3. Weird numbers: Employees has 9,999, which looks fake.
#    Employees of 0 is okay (some businesses have no workers).
# 4. Duplicates: 40 rows are exact copies.
# 5. Industry names: there are 40+ spellings instead of 8
#    (different capitals, extra spaces, typos like "Resturants").
#    Region and Loan Status are fine.

# CLEAN

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.drop_duplicates()
