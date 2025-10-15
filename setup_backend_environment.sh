#!/usr/bin/env bash
set -e

echo "=== Setting up API environment ==="

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Build database
python3 api/data/create_database/create_database.py

# navigate to api directory
cd api/

# Save data into database
python3 -m data.save_location.save_location_zone
python3 -m data.save_location.save_payment
python3 -m data.save_location.save_ratecode
python3 -m data.save_location.save_vendor
python3 -m data.save_location.save_trips

echo "Backend Environment setup complete. Running at http://localhost:8000"

# Launch backend server
python3 -m web.app
