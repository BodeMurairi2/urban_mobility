@echo off
echo === Setting up Frontend Environment ===

REM Navigate to the frontend directory
cd frontend\nyc-metropolis-taxi-analytics\

REM Start a local HTTP server on port 5500
python -m http.server 5500

echo Frontend environment setup complete. Running at http://localhost:5500
