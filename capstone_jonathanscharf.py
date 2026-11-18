import pandas as pd

df = pd.read_csv("data/capstone_finance.csv")
print(df.shape)
print(df.head())
df.info()
print(df.isnull().sum())
print(df.describe())
