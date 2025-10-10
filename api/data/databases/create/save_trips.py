#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pyarrow.parquet as pq

DB_PATH = Path("/home/bode-murairi/Documents/programming/urban_mobility/api/data/databases/create/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

# Open Parquet file with pyarrow
file_path = "/home/bode-murairi/Documents/programming/urban_mobility/api/services/extract/data_file/"
parquet_file = pq.ParquetFile(f"{file_path}/yellow_tripdata.parquet")

# Standardized column names
columns = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
    "passenger_count", "trip_distance", "RatecodeID",
    "store_and_fwd_flag", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "extra", "mta_tax",
    "tip_amount", "tolls_amount", "improvement_surcharge",
    "total_amount", "congestion_surcharge", "Airport_fee",
    "cbd_congestion_fee"
]

with engine.begin() as conn:
    # SQLite tuning
    conn.exec_driver_sql("PRAGMA synchronous = OFF")
    conn.exec_driver_sql("PRAGMA journal_mode = MEMORY")
    conn.exec_driver_sql("PRAGMA temp_store = MEMORY")
    conn.exec_driver_sql("PRAGMA cache_size = 100000")
    conn.exec_driver_sql("PRAGMA locking_mode = EXCLUSIVE")

    for i, rg in enumerate(parquet_file.iter_batches(batch_size=10000)):
        # Convert to DataFrame
        df_chunk = pd.DataFrame(rg.to_pandas())

        # -----------------------------
        # Remove duplicates and NaNs
        # -----------------------------
        df_chunk = df_chunk.drop_duplicates(ignore_index=True)
        df_chunk = df_chunk.dropna()

        # Standardize columns
        df_chunk.columns = columns

        # Save to SQLite
        df_chunk.to_sql(
            name="trips",
            con=conn,
            if_exists="append" if i > 0 else "replace",
            index=False,
            method=None
        )
        print(f"Inserted batch {i+1}")
