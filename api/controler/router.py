#!/usr/bin/env python3
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter
from services.transform.get_trips import (
    most_visited_places_bytrips,
    most_visited_places_bypopulation,
    longest_trip,
    shortest_trip,
    average_trip_summary,
    vendor_dominant_region
)

router = APIRouter()

executor = ThreadPoolExecutor()

async def run_sync(func, *args, **kwargs):
    """helper function to run synchronous function
    asynchronous
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))


@router.get("/")
async def home():
    """Home page"""
    return {
        "Message": "Welcome to NYC Analysis Dashboard",
        "Success": "success"
    }

@router.get("/visit/most_trips")
async def get_most_visited_places_bytrips():
    """Return most visited places by number of trips"""
    return await run_sync(most_visited_places_bytrips)

@router.get("/visit/most_passengers")
async def get_most_visited_places_bypopulation():
    """Return most visited places by passenger population"""
    return await run_sync(most_visited_places_bypopulation)

@router.get("/trips/shortest")
async def get_shortest_trip():
    """Return shortest trip"""
    return await run_sync(shortest_trip)

@router.get("/trips/longest")
async def get_longest_trip():
    """Return longest trip"""
    return await run_sync(longest_trip)

@router.get("/trips/average")
async def get_average_trip_distance():
    """Return average trip distance"""
    return await run_sync(average_trip_summary)

@router.get("/trips/vendor")
async def get_vendor_dominant_region():
    """Return vendor dominant regions"""
    return await run_sync(vendor_dominant_region)
