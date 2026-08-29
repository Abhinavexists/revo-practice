from aifc import Error
from pathlib import Path

import pandas as pd

data = Path("sales_data.csv")

try:
    df = pd.read_csv(data)
    print(df.head(5))
    print(df.describe)
    print(df.dtypes)
except FileNotFoundError:
    raise FileNotFoundError("data not provided")

# handle missing values
# df.isnull().any() returns True/False per column
# df.isnull().any().any() returns overall True/False
if df.isnull().any().any():
    print(df.isnull().sum())  # gives the total no. of missing values
    df_filled = df.fillna(0)  # many other ways but this is one of them
    # advised to create a copy
    # not always replaced with 0 , maybe if i want to replace a clinical value , i may use the mean of the data.
else:
    raise Error("No Null column")

# if "Sales_fillNA" in df.columns:
#     df["Sales_fillNA"] = df["Sales"].fillna(df["Sales"].mean())
# else:
#     raise Error("No Sales_fillNA column exists")

df_rename = df.rename(columns={"Date": "Sales Date"})  # renaming
print(df_rename.head())

if "Value" in df.columns:
    df["Value_new"] = df["Total Revenue"].fillna(df["Total Revenue"].mean()).astype(int)
    df["New Value"] = df["Total Revenue"].apply(lambda x: x + 2)
    print(df.head())
else:
    pass

# Data aggregation and grouping
grouped_mean = df.groupby("Product Category")["Total Revenue"].mean()
print(grouped_mean)

grouped_sum = df.groupby(["Product Category", "Region"])["Total Revenue"].sum()
print(grouped_mean)

grouped_mean = df.groupby(["Product Category", "Region"])["Total Revenue"].mean()
print(grouped_mean)

# aggregate multiple fuctions , right now before this we did single statement for each aggregation

grouped_agg = df.groupby(["Region"])["Total Revenue"].agg(["mean", "sum", "count"])
print(grouped_agg)

# Merging and joining dataframes
df1 = pd.DataFrame({"Key": ["A", "B", "C"], "Value1": [1, 2, 3]})
df2 = pd.DataFrame({"Key": ["A", "B", "D"], "Value2": [4, 5, 6]})

print(df1)
print(df2)

# Key is the column on which joining
merged_df_inner = pd.merge(df1, df2, on="Key", how="inner")  # inner join
merged_df_outer = pd.merge(df1, df2, on="Key", how="outer")  # outer join
merged_df_left = pd.merge(df1, df2, on="Key", how="left")  # left join
merged_df_right = pd.merge(df1, df2, on="Key", how="right")  # right join

print(merged_df_inner)
print(merged_df_outer)
print(merged_df_left)
print(merged_df_right)
