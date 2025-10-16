---

# NYC Yellow Taxi Data Analysis Web Application

This project **analyzes and visualizes NYC Yellow Taxi data** through an interactive web application. Please read and follow each step carefully.

---
## Video Presentation
Link: https://youtu.be/Xak9DxeP_M8

## Link to the documentation
Link https://docs.google.com/document/d/1BFFyp-8KrrF6fp8xCNjIDEi-zjtFKBDLrUf7OTnEiD4/edit?usp=sharing

## System Architecture
cd urban_mobility/system_architecture/
Urban Mobility System Architecture.jpg

## Technology Stack

* **Frontend:** HTML5, CSS, JavaScript
* **Backend:** FastAPI
* **Database:** SQLite3

---

## Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/BodeMurairi2/urban_mobility.git
cd urban_mobility/
```

---

### 2️⃣ Linux / macOS Setup

**Backend:**

```bash
# Run backend setup script at the root of the repository
./setup_backend_environment.sh
```

**Frontend:**

```bash
# Open a new terminal in the project root
./setup_frontend_environment.sh
```

**Visit the application:**

```
http://127.0.0.1:5500
```

---

### 3️⃣ Windows Setup (Git Bash)

**Backend Setup:**

```bash
# using cmd termianl, change to project repository
cd urban_mobility/
run:
windows_setup.cmd
to reopen the backend server:
cd urban_mobility/api/
check if virtual environment is open. If not,:
inside urban_mobility/, run:
.\venv\Scripts\activate, then
cd api/, run:
python -m web.app

# using git bash terminal, run the following commands
python -m venv venv
source venv/Scripts/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build the database
python api/data/create_database/create_database.py

# Navigate to API directory and populate data
cd api/
python -m data.save_location.save_location_zone
python -m data.save_location.save_payment
python -m data.save_location.save_ratecode
python -m data.save_location.save_vendor
python -m data.save_location.save_trips

# Start backend server
python -m web.app
```

**Frontend Setup:**

```bash
# Open a new terminal
cd frontend/nyc-metropolis-taxi-analytics/
python -m http.server 5500
```

**Frontend URL:**

```
cd frontend/nyc-metropolis-taxi-analytics/  # using git bash terminal
cd frontend\nyc-metropolis-taxi-analytics\  # using cmd terminal
http://127.0.0.1:5500
```

## Notes:
```
Pages take time (latency time) to load due to computation happening inside the backend (with pandas) and update happening on the frontend. Wait few seconds to see the updates on the pages
```

## Project Structure

```
urban_mobility/
├─ api/                   # Backend code
│  ├─ data/               # Data processing scripts
|  |--services/           # Business logics and computations layer
|  |--logs/               # Logs for requests
|  |-- database/          # Database folder database/instance/api
|  |-- controler/         # Redirect requests to appropriate endpoint
|  |-- dsa                # Data Structure and algorithm implementation
│  └─ web/                # FastAPI app
├─ frontend/              # Frontend code (HTML, CSS, JS)
├─ database/              # SQLite database files
├─ setup_backend_environment.sh
├─ setup_frontend_environment.sh
└─ README.md
```

---
---

## Features

* Analyze NYC Yellow Taxi trip data
* Populate database from raw data after cleaning and ETL
* Interactive frontend visualization
* REST API
---

## Contributors

* **Bode Murairi** – [b.murairi@alustudent.com](mailto:b.murairi@alustudent.com)
* **Maurice Nshimyumukiza** – [m.nshimyumu@alustudent.com](mailto:m.nshimyumu@alustudent.com)
* **Pascal Louis Nsigo** – [p.nsigo@alustudent.com](mailto:p.nsigo@alustudent.com)

## Incase of anything, please carefully read this document again, or contact any of the contributors.
