import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import pyarrow.parquet as pq

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "databases"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "trips.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Open Parquet file with pyarrow
parquet_file = pq.ParquetFile("urban_mobility.parquet")

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
        df_chunk = pd.DataFrame(rg.to_pandas())
        df_chunk = df_chunk.drop_duplicates(ignore_index=True).dropna()
        df_chunk.columns = columns
        df_chunk.to_sql(
            name="trips",
            con=conn,
            if_exists="append" if i > 0 else "replace",
            index=False,
            method=None
        )
        print(f"Inserted batch {i+1}")
