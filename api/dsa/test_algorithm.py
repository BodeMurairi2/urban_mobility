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

# create a session
session = Session()

def test_dictionary_lookup():
    """This function takes the spead of a 
    search algorithm with dictionary lookup
    """
    load_data = [(zone.location_id, zone) for zone in session.query(TaxiZones).all()]
    
    target_id = 250
    start_time = time.time()
    
    found = None
    for key, value in load_data:
        if key == target_id:
            found = value
            break
    
    end_time = time.time()
    
    if found:
        print("Found data:", found)
    else:
        print("Data not found")
    
    print("Elapsed time:", end_time - start_time)
    return

def linear_search():
    """This function measures the speed of a linear search algorithm"""
    load_data = session.query(TaxiZones).all()
    start_time = time.time()
    
    for zone in load_data:
        if zone.location_id == 250:
            print("Found data")
    
    end_time = time.time()
    print("Elapsed time:", end_time - start_time)
    return

test_dictionary_lookup()
linear_search()
