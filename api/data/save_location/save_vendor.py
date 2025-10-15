#!/usr/bin/env python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from data.create_database.models import Vendors

# Setup database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

session = Session()

def save_vendors():
    try:
        vendors = [
            Vendors(vendor_id=1, vendor_name='Creative Mobile Technologies'),
            Vendors(vendor_id=2, vendor_name='VeriFone Inc'),
            Vendors(vendor_id=3, vendor_name='UNKNOWN'),
            Vendors(vendor_id=4, vendor_name='UNKWOWN'),
            Vendors(vendor_id=5, vendor_name='UNKWOWN'),
            Vendors(vendor_id=6, vendor_name='UNKWOWN'),
            Vendors(vendor_id=7, vendor_name='UNKWOWN')
        ]

        session.add_all(vendors)
        session.commit()
        print("Vendors successfully inserted.")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error inserting vendors:", e)
    finally:
        session.close()

if __name__ == "__main__":
    save_vendors()
