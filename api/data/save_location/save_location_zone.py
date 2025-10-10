#!/usr/bin/env python3
"""This script saves Taxi Zone Locations to the database"""
from pathlib import Path
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import TaxiZones
from base import Base  # in case relationships need it

# -----------------------------
# Setup database
# -----------------------------
DB_PATH = Path("/home/bode-murairi/Documents/programming/urban_mobility/api/data/databases/create/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

# Load CSV file (dynamic path)
DEFAULT_CSV_PATH = Path("/home/bode-murairi/Documents/programming/urban_mobility/api/services/extract/data_file/taxi_zone_lookup.csv")
CSV_PATH = Path(os.getenv("TAXI_CSV_PATH", str(DEFAULT_CSV_PATH)))

print(f"Using CSV path: {CSV_PATH}")

if not CSV_PATH.exists():
    raise FileNotFoundError(f"DATA file not found: {CSV_PATH}")

data = pd.read_csv(CSV_PATH)
print("Columns found:", data.columns.to_list())

# Save function
def save_to_database(csv_file: pd.DataFrame):
    """Save taxi zones to the database without duplicates"""
    session = Session()
    try:
        for borough, zone, service_zone in zip(
            csv_file["Borough"].tolist(),
            csv_file["Zone"].tolist(),
            csv_file["service_zone"].tolist()
        ):
            exists = session.query(TaxiZones).filter_by(
                borough=borough, zone=zone, service_zone=service_zone
            ).first()
            if exists:
                continue

            new_location = TaxiZones(
                borough=borough,
                zone=zone,
                service_zone=service_zone
            )
            session.add(new_location)

        session.commit()
        return "Data saved successfully"

    except SQLAlchemyError as error:
        session.rollback()
        return f"Error occurred: {error}"

    finally:
        session.close()

# Run script
if __name__ == "__main__":
    result = save_to_database(csv_file=data)
