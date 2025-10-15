Absolutely! Here’s a polished, visually appealing version of your README using Markdown with **sections, code blocks, badges, and lists** for clarity:

---

# 🟡 NYC Yellow Taxi Data Analysis Web Application

This project **analyzes and visualizes NYC Yellow Taxi data** through an interactive web application.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS, JavaScript
* **Backend:** FastAPI
* **Database:** SQLite3

---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/BodeMurairi2/urban_mobility.git
cd urban_mobility/
```

---

### 2️⃣ Linux / macOS Setup

**Backend:**

```bash
# Run backend setup script
./setup_backend_environment.sh
```

**Frontend:**

```bash
# Open a new terminal in the project root
./setup_frontend_environment.sh
```

**Visit the application:**

```
http://127.0.0.1:5500/
open index.html
```

---

### 3️⃣ Windows Setup (Git Bash)

**Backend Setup:**

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/Scripts/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build the database
python3 api/data/create_database/create_database.py

# Navigate to API directory and populate data
cd api/
python3 -m data.save_location.save_location_zone
python3 -m data.save_location.save_payment
python3 -m data.save_location.save_ratecode
python3 -m data.save_location.save_vendor
python3 -m data.save_location.save_trips

# Start backend server
python3 -m web.app
```

**Frontend Setup:**

```bash
# Open a new terminal
cd urban_mobility/frontend
python3 -m http.server 5500
```

**Frontend URL:**

```
http://127.0.0.1:5500
```

---

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

