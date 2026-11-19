import pandas as pd

df = pd.read_csv("data/capstone_finance.csv")
print(df.shape)
print(df.head())
df.info()
print(df.isnull().sum())
print(df.describe())

# -- M13: DATA QUALITY ISSUES (raw: 5,000 rows x 11 columns) --
# 1. Blank cells: Region (128), Credit Score (91), Application Date (30)
# 2. Wrong types: Loan Amount and Profit are text because of "$" and ",".
#    Application Date is text, not a date.
# 3. Weird numbers: Employees has 9,999, which looks fake.
#    Employees of 0 is okay (some businesses have no workers).
# 4. Duplicates: 40 rows are exact copies.
# 5. Industry names: there are 40+ spellings instead of 8
#    (different capitals, extra spaces, typos like "Resturants").
#    Region and Loan Status are fine.

# -----CLEAN----- 

df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.drop_duplicates()
print("After duplicates:", df.shape)

# Section 3

# Money: loan_amount and profit are text because of $ and ,
# Remove them and convert to numbers (negatives stay negative)
for col in ["loan_amount", "profit"]:
    df[col] = df[col].str.replace("$", "", regex=False)
    df[col] = df[col].str.replace(",", "", regex=False).astype(float)

# (MM/DD/YYYY and "March 29 2025"); junk and impossible dates stay NaT.
raw_dates = df["application_date"].copy()
d1 = pd.to_datetime(raw_dates, errors="coerce")
d2 = pd.to_datetime(raw_dates, format="%m/%d/%Y", errors="coerce")
d3 = pd.to_datetime(raw_dates, format="%B %d %Y", errors="coerce")
df["application_date"] = d1.fillna(d2).fillna(d3)

bad = raw_dates[df["application_date"].isna() & raw_dates.notna()]
print(len(bad))
print(bad.value_counts())

print(df[["loan_amount", "profit"]].dtypes)
print(df[["loan_amount", "profit"]].head())
print(df["application_date"].dtype)
print("NaT count:", df["application_date"].isna().sum())