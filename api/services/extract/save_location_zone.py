#!/usr/bin/env python3
"""This script saves Taxi Zone Locations to the database"""
from pathlib import Path
import pandas as pd
from simpledbf import Dbf5
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import TaxiZones

# setup database
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "databases"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "trips.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

# load csv file
CSV_PATH = BASE_DIR / "taxi_zone_lookup.csv"
if not CSV_PATH.exists():
    raise FileNotFoundError(f"DATA file not found: {CSV_PATH}")

data = pd.read_csv(CSV_PATH)

print(data.columns.to_list())

# save function
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

if __name__ == "__main__":
    result = save_to_database(csv_file=data)
    print(result)
