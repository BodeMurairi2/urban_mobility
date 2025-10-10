#!/usr/bin/python3
from services.extract.extract_trips import (
    get_most_visited_places_bytrips,
    get_most_visited_places_bypopulation,
    find_longest_trip,
    find_shortest_trip,
    vendor_dominate_region,
    average_trip_distance,
)

def most_visited_places_bytrips():
    """Most visited places by trips"""
    df = get_most_visited_places_bytrips()
    return df.to_dict(orient="records")

def most_visited_places_bypopulation():
    """Most visited places by population"""
    df = get_most_visited_places_bypopulation()
    return df.to_dict(orient="records")

def longest_trip():
    """Get longest trip"""
    df = find_longest_trip()
    return df.to_dict(orient="records")

def shortest_trip():
    """Get shortest trip"""
    df = find_shortest_trip()
    return df.to_dict(orient="records")

def average_trip_summary():
    """Get average trip"""
    avg = average_trip_distance()
    return {"average_trip_distance": avg}

def vendor_dominant_region():
    """Get vendor dominant regions"""
    df = vendor_dominate_region()
    return df.to_dict(orient="records")

if __name__ == "__main__":
    print(most_visited_places_bytrips())
    print(most_visited_places_bypopulation())
    print(longest_trip())
    print(shortest_trip())
    print(average_trip_summary())
    print(vendor_dominant_region())
