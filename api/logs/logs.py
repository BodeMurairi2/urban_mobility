#!/usr/bin/env python3
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
import time
from fastapi import APIRouter, Request
from services.transform.get_trips import (
    most_visited_places_bytrips,
    most_visited_places_bypopulation,
    longest_trip,
    shortest_trip,
    average_trip_summary,
    vendor_dominant_region
)

# logger configuration
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
logger.propagate = False

# Absolute path to log file
log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "api_logs.log"))

# file handler
file_handler = logging.FileHandler(log_file_path, mode="a")
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)

# Ensure handlers are added only once
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Router
router = APIRouter()
executor = ThreadPoolExecutor()

# run sync function asynchronously
async def run_sync(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))


# log request execution
async def log_request(request: Request, start_time: float):
    """log request"""
    duration = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url} completed in {duration:.3f}s")


# helper: endpoint wrapper
async def handle_endpoint(request: Request, func, description: str):
    """helper function"""
    start_time = time.time()
    try:
        result = await run_sync(func)
        logger.info(f"{description} - Success")
        await log_request(request, start_time)
        return result
    except Exception as e:
        logger.error(f"{description} - Error: {e}")
        await log_request(request, start_time)
        return {"error": str(e)}

# endpoints
@router.get("/")
async def home(request: Request):
    """home function"""
    start_time = time.time()
    logger.info("Home endpoint accessed")
    await log_request(request, start_time)
    return {"Message": "Welcome to NYC Analysis Dashboard", "Success": "success"}

@router.get("/visit/most_trips")
async def get_most_visited_places_bytrips(request: Request):
    """logs for most visited places by trips"""
    return await handle_endpoint(request, most_visited_places_bytrips, "Most visited places by trips")

@router.get("/visit/most_passengers")
async def get_most_visited_places_bypopulation(request: Request):
    """logs for passangers"""
    return await handle_endpoint(request, most_visited_places_bypopulation, "Most visited places by population")

@router.get("/trips/shortest")
async def get_shortest_trip(request: Request):
    """logs for shortest trip"""
    return await handle_endpoint(request, shortest_trip, "Shortest trip")

@router.get("/trips/longest")
async def get_longest_trip(request: Request):
    """loggs for longest trip"""
    return await handle_endpoint(request, longest_trip, "Longest trip")

@router.get("/trips/average")
async def get_average_trip_distance(request: Request):
    """Logs for average"""
    return await handle_endpoint(request, average_trip_summary, "Average trip distance")

@router.get("/trips/vendor")
async def get_vendor_dominant_region(request: Request):
    """loggs for vendor"""
    return await handle_endpoint(request, vendor_dominant_region, "Vendor dominant region")
