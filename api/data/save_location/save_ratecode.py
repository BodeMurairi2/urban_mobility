#!/usr/bin/env python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from data.create_database.models import RateCodes

# Setup database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

session = Session()

def save_rate_codes():
    try:
        rate_codes = [
            RateCodes(rate_code_id=1, description='Standard rate – regular metered fare within NYC'),
            RateCodes(rate_code_id=2, description='JFK – flat rate trip to/from JFK Airport'),
            RateCodes(rate_code_id=3, description='Newark – trips to Newark Airport'),
            RateCodes(rate_code_id=4, description='Nassau or Westchester – trips beyond NYC limits to these counties'),
            RateCodes(rate_code_id=5, description='Negotiated fare – fare agreed upon before trip (not metered)'),
            RateCodes(rate_code_id=6, description='Group ride – multiple passengers sharing a taxi (split fare)')
        ]
        
        session.add_all(rate_codes)
        session.commit()
        print("Rate codes successfully inserted.")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error inserting rate codes:", e)
    finally:
        session.close()

if __name__ == "__main__":
    save_rate_codes()
