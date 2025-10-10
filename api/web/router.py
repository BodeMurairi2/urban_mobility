#!/usr/bin/env python3
from fastapi import APIRouter
from services.transform.get_trips import (
    most_visited_places_bytrips,
    most_visited_places_bypopulation,
    longest_trip,
    shortest_trip,
    average_trip_summary,
    vendor_dominant_region,
)

router = APIRouter()

@router.get("/")
async def home():
    return {
        "Message": "Welcome to NYC Analysis Dashboard",
        "Success": "success"
    }

@router.get("/visit/most_trips")
async def get_most_visited_places_bytrips():
    """Return most visited places by number of trips"""
    return most_visited_places_bytrips()

@router.get("/visit/most_passengers")
async def get_most_visited_places_bypopulation():
    """Return most visited places by passenger population"""
    return most_visited_places_bypopulation()

@router.get("/trips/shortest")
async def get_shortest_trip():
    """Return shortest trip"""
    return shortest_trip()

@router.get("/trips/longest")
async def get_longest_trip():
    """Return longest trip"""
    return longest_trip()

@router.get("/trips/average")
async def get_average_trip_distance():
    """Return average trip distance"""
    return average_trip_summary()

@router.get("/trips/vendor")
async def get_vendor_dominant_region():
    """Return vendor dominant regions"""
    return vendor_dominant_region()
