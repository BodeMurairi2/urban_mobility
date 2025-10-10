#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

@app.get("/")
async def home():
    return {
        "message": "Welcome to NYC Analyzis",
        "status": "Success"
    }

@app.get("/dashboard")
async def dashboard():
    return {
        "message": "This is our dashboard",
        "success": True
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        port=8000
    )
