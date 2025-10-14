#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controler.router import router as api_router

app = FastAPI(
    title="NYC Taxi Trip Analysis",
    description="Dashboard API for NYC Yellow Taxi Dataset",
    version="1.0.0",
)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "NYC Taxi API is running!"}

if __name__ == "__main__":
    uvicorn.run(
        "web.app:app",
        port=8000,
        reload=True
    )
