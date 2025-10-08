from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trips = [
    {"passenger_count": 2, "duration": 12, "pickup_location": "Manhattan", "dropoff_location": "Brooklyn"},
    {"passenger_count": 1, "duration": 8, "pickup_location": "Queens", "dropoff_location": "Manhattan"},
    {"passenger_count": 3, "duration": 20, "pickup_location": "Bronx", "dropoff_location": "Manhattan"},
    {"passenger_count": 1, "duration": 15, "pickup_location": "Manhattan", "dropoff_location": "Queens"},
    {"passenger_count": 2, "duration": 10, "pickup_location": "Brooklyn", "dropoff_location": "Manhattan"}
]

@app.get("/")
async def home():
    return {"message": "Welcome to NYC Taxi Analytics"}

@app.get("/trips")
async def get_trips():
    return {"trips": trips}

@app.get("/dashboard")
async def dashboard():
    total_trips = len(trips)
    avg_duration = sum(t["duration"] for t in trips) / total_trips
    avg_passengers = sum(t["passenger_count"] for t in trips) / total_trips
    return {
        "total_trips": total_trips,
        "avg_duration": round(avg_duration, 2),
        "avg_passengers": round(avg_passengers, 2)
    }
