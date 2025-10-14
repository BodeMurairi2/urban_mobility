import pandas as pd

file_path = "data/yellow_tripdata_2025-01.parquet"

df = pd.read_parquet(file_path)
print("rows:",len(df))
print("columns:", list(df.columns))

df.dropna(inplace=True)

print("rows:",len(df))
print("columns:", list(df.columns))

df.drop_duplicates(inplace=True)
print(df.duplicated().sum())

df.drop(df[df['trip_distance'] < 0].index, inplace=True)
print("rows:",len(df))
print("columns:", list(df.columns))


