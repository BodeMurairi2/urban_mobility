#!/usr/bin/env python3

import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from data.create_database.models import TaxiZones

# Setup database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)
session = Session()

def key_value_search(test_id: int) -> None:
    """Manually implemented key-value search (simulating a dictionary lookup)"""
    load_data = [(zone.location_id, zone) for zone in session.query(TaxiZones).all()]
    start_time = time.time()

    found = None
    for key, value in load_data:
        if key == test_id:
            found = value
            break

    end_time = time.time()

    if found:
        print("Found data")
    else:
        print("Data not found")

    print(f"Key-Value Search Elapsed time: {end_time - start_time:.8f} seconds\n")

def linear_search(test_id: int) -> None:
    """Manually implemented linear search"""
    load_data = session.query(TaxiZones).all()
    start_time = time.time()

    found = None
    for zone in load_data:
        if zone.location_id == test_id:
            found = zone
            break

    end_time = time.time()

    if found:
        print("Found data")
    else:
        print("Data not found")

    print(f"Linear Search Elapsed time: {end_time - start_time:.8f} seconds\n")


if __name__ == "__main__":
    test_cases = [1, 5, 10, 50, 100, 150, 200, 225, 250, 300]

    for test_id in test_cases:
        print(f"Testing with ID = {test_id}")
        key_value_search(test_id)
        linear_search(test_id)
