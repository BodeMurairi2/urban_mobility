#!/usr/bin/env python3

import os
import pandas as pd
from .clean_data import clean_dataset

# load the data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "yellow_tripdata.parquet")

# Load the data
data = pd.read_parquet(DATA_PATH)
clean_data = clean_dataset(data=data)

def get_most_visited_places_bytrips():
    """Most visited places by trips"""
    data = pd.read_parquet(DATA_PATH)
    clean_data = data.dropna()
    most_visited_places = (
    clean_data.groupby("DOLocationID")["passenger_count"]
    .count()
    .reset_index(name="NumTrips")
    .sort_values("NumTrips", ascending=False)
    )
    return most_visited_places.head(10)

def get_most_visited_places_bypopulation():
    """get the most visited places based on the number of passangers"""
    data = pd.read_parquet(DATA_PATH)
    clean_data = data.dropna()
    most_visited_places = (
    clean_data.groupby("DOLocationID")["passenger_count"]
    .sum()
    .reset_index(name="PassangerCount")
    .sort_values("PassangerCount", ascending=False)
    )
    return most_visited_places.head(10)

def new_datatime_clean():
    """ trip duration studies"""
    data = pd.read_parquet(DATA_PATH)
    clean_data = data.dropna().copy()
    clean_data["trip_duration"] = clean_data["tpep_dropoff_datetime"] - clean_data["tpep_pickup_datetime"]
    return clean_data

def find_longest_trip():
    """find the longest_trip"""
    clean_data = new_datatime_clean()
    longest_trip_index = clean_data["trip_distance"].idxmax()
    longest_trip_row_df = clean_data.loc[[longest_trip_index]]
    return longest_trip_row_df

def find_shortest_trip():
    """Find shortest trip"""
    clean_data = new_datatime_clean()
    shortest_trip_idx = clean_data["trip_distance"].idxmin()
    shortest_trip = clean_data.loc[[shortest_trip_idx]]
    return shortest_trip

def average_trip_distance():
    """"find average trip distance"""
    clean_data = new_datatime_clean()
    return clean_data["trip_distance"].mean()

def average_total_price():
    """find average total trip price and total passanger count"""
    clean_data = new_datatime_clean()
    positive_price = clean_data[clean_data["total_amount"] > 0]
    return (positive_price["total_amount"].mean(),
            positive_price["total_amount"].max(),
            positive_price["total_amount"].min(),
            clean_data["passenger_count"].sum()
            )

def vendor_dominate_region():
    """Most dominate region by vendor ID"""
    data = pd.read_parquet(DATA_PATH)
    clean_data = data.dropna()
    vendor_counts = clean_data.groupby(["PULocationID", "VendorID"]).size().reset_index(name="trip_count")

    dominant_vendors = vendor_counts.loc[vendor_counts.groupby("PULocationID")["trip_count"].idxmax()].sort_values("trip_count", ascending=False)

    return dominant_vendors.head(10)

if __name__ == "__main__":
    get_most_visited_places_bytrips()
    get_most_visited_places_bypopulation()
    new_datatime_clean()
    find_longest_trip()
    find_shortest_trip()
    average_trip_distance()
    vendor_dominate_region()
