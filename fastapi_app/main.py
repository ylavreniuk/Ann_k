from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
import asyncpg
import json
import jwt
import os

from .routers import events, calendars, availability
from .database import get_db
from .auth import get_current_user

app = FastAPI(title="Booking API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(calendars.router, prefix="/api/v1/calendars", tags=["calendars"])
app.include_router(availability.router, prefix="/api/v1/availability", tags=["availability"])

@app.get("/")
async def root():
    return {"message": "Booking API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "booking-api"}

# WebSocket для real-time оновлень
@app.websocket("/ws/calendar/{calendar_id}")
async def websocket_calendar_updates(
    websocket: WebSocket,
    calendar_id: str
):
    await websocket.accept()
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except:
        await websocket.close()