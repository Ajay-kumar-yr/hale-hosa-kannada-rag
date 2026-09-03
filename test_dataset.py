import pandas as pd

df = pd.read_csv("data/train_final.csv")

print("Columns:")
print(df.columns.tolist())

print("\nNumber of rows:")
print(len(df))

print("\nFirst 5 rows:")
print(df.head())