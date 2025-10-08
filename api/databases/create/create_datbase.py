#!/usr/bin/env python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import models  # import your models so Base.metadata sees all tables

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "databases", "trips.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(f"Database created successfully at {DB_PATH}")
