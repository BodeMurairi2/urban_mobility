#!/usr/bin/python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from data.create_database.models import TaxiZones
from services.extract.extract_trips import (
    get_most_visited_places_bytrips,
    get_most_visited_places_bypopulation,
    find_longest_trip,
    find_shortest_trip,
    vendor_dominate_region,
    average_trip_distance,
    average_total_price
)

# Setup database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/instance/trips.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=engine)

session = Session()

def most_visited_places_bytrips() -> dict:
    """Most visited places by trips"""
    df = get_most_visited_places_bytrips()
    most_visited_trips = df.to_dict(orient="records")
    for places_id in most_visited_trips:
        destination = session.query(TaxiZones).where(TaxiZones.location_id==places_id["DOLocationID"]).first()
        if destination:
            places_id["DOLocationName"] = destination.borough
            places_id["Zone"] = destination.zone
            places_id["serviceZone"] = destination.service_zone
    
    return most_visited_trips

def most_visited_places_bypopulation() -> dict:
    """Most visited places by population"""
    df = get_most_visited_places_bypopulation()
    most_visited_trips = df.to_dict(orient="records")
    for places_id in most_visited_trips:
        destination = session.query(TaxiZones).where(TaxiZones.location_id==places_id["DOLocationID"]).first()
        if destination:
            places_id["DOLocationName"] = destination.borough
            places_id["Zone"] = destination.zone
            places_id["serviceZone"] = destination.service_zone
    
    return most_visited_trips

def longest_trip() -> dict:
    """Get longest trip"""
    df = find_longest_trip()
    longest_trip_data = df.to_dict(orient="records")
    zones = {location.location_id: location for location in session.query(TaxiZones).all()}
    for trip in longest_trip_data:
        pickup_data = zones.get(trip["PULocationID"])
        destination_data = zones.get(trip["DOLocationID"])
        if pickup_data:
            trip["PULocationName"] = pickup_data.borough
            trip["PULocationZone"] = pickup_data.zone

        if destination_data:
            trip["DOLocationName"] = destination_data.borough
            trip["DOLocationZone"] = destination_data.zone

    return longest_trip_data

def shortest_trip() -> dict:
    """Get shortest trip"""
    df = find_shortest_trip()
    shortest_trip_data = df.to_dict(orient="records")
    zones = {location.location_id: location for location in session.query(TaxiZones).all()}
    for trip in shortest_trip_data:
        pickup_data = zones.get(trip["PULocationID"])
        destination_data = zones.get(trip["DOLocationID"])
        if pickup_data:
            trip["PULocationName"] = pickup_data.borough
            trip["PULocationZone"] = pickup_data.zone

        if destination_data: 
            trip["DOLocationName"] = destination_data.borough
            trip["DOLocationZone"] = destination_data.zone

    return shortest_trip_data

def average_trip_summary() -> dict:
    """Get average trip information"""
    avg_distance = float(average_trip_distance())
    avgs = average_total_price()
    return {"average_trip_distance": f"{avg_distance:.3f} Km",
            "highest_ticket_price": f"{avgs[1]:.2f}$",
            "smallest_ticket_price": f"{avgs[2]:.2f}$",
            "average_total_price": f"{avgs[0]:.2f}$",
            "total_number_passanger": f"{avgs[3]} passangers"
            }

def vendor_dominant_region() -> dict:
    """Get vendor dominant regions"""
    zones = {location.location_id: location for location in session.query(TaxiZones).all()}
    df = vendor_dominate_region()
    vendor_data = df.to_dict(orient="records")
    for trip in vendor_data:
        pu_data = zones.get(trip["PULocationID"])
        if pu_data:
            trip["PULocationName"] = pu_data.borough
            trip["PULocationZone"] = pu_data.zone
            trip["VendorName"] = "VeriFone Inc"
    return vendor_data

if __name__ == "__main__":
    print(most_visited_places_bytrips())
    print(most_visited_places_bypopulation())
    print(longest_trip())
    print(shortest_trip())
    print(average_trip_summary())
    print(vendor_dominant_region())
