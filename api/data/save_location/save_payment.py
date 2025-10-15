#!/usr/bin/env python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from data.create_database.models import PaymentTypes

# Setup database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

session = Session()

def save_payment():
    try:
        payments = [
            PaymentTypes(payment_type_id=1, description='Credit card'),
            PaymentTypes(payment_type_id=2, description='Cash'),
            PaymentTypes(payment_type_id=3, description='No charge (e.g., free trips, promo rides)'),
            PaymentTypes(payment_type_id=4, description='Dispute (fare not paid due to passenger dispute)'),
            PaymentTypes(payment_type_id=5, description='Unknown'),
            PaymentTypes(payment_type_id=6, description='Voided trip (trip canceled or voided before completion)')
        ]
        
        session.add_all(payments)
        session.commit()
        print("Payment types successfully inserted.")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error inserting payment types:", e)
    finally:
        session.close()

if __name__ == "__main__":
    save_payment()
