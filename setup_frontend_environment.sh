#!/usr/bin/env bash

# setup the frontend
cd /frontend/nyc-metropolis-taxi-analytics/
python3 -m http.server 5500

echo "Frontend environment setup. Frontend is running at http://localhost:5500"
